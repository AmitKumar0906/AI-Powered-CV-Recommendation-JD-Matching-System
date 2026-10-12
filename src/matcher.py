"""
matcher.py: Embedding generation, Cosine Similarity, and Hybrid Recommendation Engine.
"""

from typing import Any, Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class CandidateMatcher:
    """Computes semantic similarity, skill overlap, and composite ranking scores."""

    _model: Optional[SentenceTransformer] = None

    @classmethod
    def get_model(cls, model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
        """Singleton pattern for loading SentenceTransformer model efficiently."""
        if cls._model is None:
            cls._model = SentenceTransformer(model_name)
        return cls._model

    @classmethod
    def compute_embedding(cls, text: str) -> np.ndarray:
        """Generate dense vector embedding for input text."""
        model = cls.get_model()
        return model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    @classmethod
    def compute_batch_embeddings(cls, texts: List[str]) -> np.ndarray:
        """Batch encode list of texts for faster vectorized inference."""
        model = cls.get_model()
        return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)

    @staticmethod
    def calculate_skill_score(candidate_skills: List[str], jd_skills: List[str]) -> Dict[str, Any]:
        """
        Calculate skill match percentage, matched skills, and missing skills.
        """
        cand_set = set(s.lower() for s in candidate_skills)
        jd_set = set(s.lower() for s in jd_skills)

        if not jd_set:
            return {
                "score": 80.0,
                "matched_skills": candidate_skills,
                "missing_skills": []
            }

        jd_dict = {s.lower(): s for s in jd_skills}
        cand_dict = {s.lower(): s for s in candidate_skills}

        matched_lower = cand_set.intersection(jd_set)
        missing_lower = jd_set.difference(cand_set)

        matched = sorted([jd_dict.get(k, k.title()) for k in matched_lower])
        missing = sorted([jd_dict.get(k, k.title()) for k in missing_lower])

        overlap_ratio = len(matched_lower) / len(jd_set)
        # Calibrated ATS skill curve: matching 5 of 10 skills is a 70.7% skill fit rather than a punishing 50%
        score = round((overlap_ratio ** 0.5) * 100.0, 1)

        return {
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing
        }

    @staticmethod
    def calculate_experience_score(candidate_exp: float, jd_min_exp: float) -> float:
        """
        Calculate experience fit score (0 - 100).
        """
        if jd_min_exp <= 0:
            return 100.0
        if candidate_exp >= jd_min_exp:
            return 100.0
        # Proportional credit if slightly below required years
        ratio = candidate_exp / jd_min_exp
        return round(max(40.0, ratio * 100.0), 1)

    @classmethod
    def rank_candidates(
        cls,
        parsed_resumes: List[Dict[str, Any]],
        parsed_jd: Dict[str, Any],
        semantic_weight: float = 0.50,
        skill_weight: float = 0.35,
        experience_weight: float = 0.15
    ) -> List[Dict[str, Any]]:
        """
        Rank a collection of parsed resumes against a Job Description using hybrid scoring.
        """
        if not parsed_resumes:
            return []

        # 1. Semantic Embedding & Cosine Similarity
        jd_text = parsed_jd.get("raw_text", "")
        jd_embedding = cls.compute_embedding(jd_text).reshape(1, -1)

        resume_texts = [r.get("raw_text", "") for r in parsed_resumes]
        resume_embeddings = cls.compute_batch_embeddings(resume_texts)

        cosine_sims = cosine_similarity(resume_embeddings, jd_embedding).flatten()

        # 2. Compute Hybrid Scores for each candidate
        jd_skills = parsed_jd.get("required_skills", [])
        jd_min_exp = parsed_jd.get("min_experience_years", 0.0)

        results = []
        for idx, resume in enumerate(parsed_resumes):
            # Semantic Similarity (0 to 1 -> 0 to 100%)
            raw_semantic = float(cosine_sims[idx])
            # Bound cosine similarity to positive percentage
            semantic_score = round(max(0.0, min(1.0, raw_semantic)) * 100.0, 1)

            # Skill overlap
            skill_info = cls.calculate_skill_score(resume.get("skills", []), jd_skills)
            skill_score = skill_info["score"]

            # Experience score
            candidate_exp = resume.get("experience_years", 0.0)
            exp_score = cls.calculate_experience_score(candidate_exp, jd_min_exp)

            # Composite weighted match score
            total_weight = semantic_weight + skill_weight + experience_weight
            composite_score = round(
                (
                    (semantic_score * semantic_weight)
                    + (skill_score * skill_weight)
                    + (exp_score * experience_weight)
                ) / total_weight,
                1
            )

            results.append({
                "candidate_name": resume.get("name", f"Candidate {idx+1}"),
                "filename": resume.get("filename", ""),
                "email": resume.get("email", ""),
                "phone": resume.get("phone", ""),
                "composite_score": composite_score,
                "semantic_score": semantic_score,
                "skill_score": skill_score,
                "experience_score": exp_score,
                "experience_years": candidate_exp,
                "education": resume.get("education", []),
                "candidate_skills": resume.get("skills", []),
                "matched_skills": skill_info["matched_skills"],
                "missing_skills": skill_info["missing_skills"],
                "raw_text": resume.get("raw_text", "")
            })

        # 3. Sort by composite score descending
        results.sort(key=lambda x: x["composite_score"], reverse=True)

        # Assign Rank
        for rank, res in enumerate(results, start=1):
            res["rank"] = rank

        return results
