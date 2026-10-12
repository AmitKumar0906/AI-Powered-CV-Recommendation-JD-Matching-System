"""
explainer.py: Explainable AI & GenAI rationale generation for candidate recommendations.
"""

import os
from typing import Any, Dict, Optional


class RecommendationExplainer:
    """Generates structured explainability and GenAI shortlisting rationale for candidates."""

    @staticmethod
    def get_verdict(composite_score: float) -> Dict[str, str]:
        """Classify recommendation into actionable recruiter verdict."""
        if composite_score >= 75.0:
            return {
                "badge": "⭐ Highly Recommended",
                "color": "#10B981",  # emerald green
                "status": "Strong Match"
            }
        elif composite_score >= 60.0:
            return {
                "badge": "✅ Recommended",
                "color": "#3B82F6",  # blue
                "status": "Good Match"
            }
        elif composite_score >= 45.0:
            return {
                "badge": "⚠️ Consider with Review",
                "color": "#F59E0B",  # amber
                "status": "Moderate Match"
            }
        else:
            return {
                "badge": "❌ Not Shortlisted",
                "color": "#EF4444",  # red
                "status": "Low Match"
            }

    @classmethod
    def generate_rationale(cls, candidate: Dict[str, Any], jd_title: str, min_exp: float) -> str:
        """
        Generate structured, recruiter-ready natural language justification.
        Deterministic and instant (zero latency / no API key required).
        """
        name = candidate.get("candidate_name", "Candidate")
        score = candidate.get("composite_score", 0.0)
        semantic = candidate.get("semantic_score", 0.0)
        skill_score = candidate.get("skill_score", 0.0)
        cand_exp = candidate.get("experience_years", 0.0)
        matched_skills = candidate.get("matched_skills", [])
        missing_skills = candidate.get("missing_skills", [])

        # Build bullet points
        points = []

        # 1. Experience assessment
        if min_exp > 0:
            if cand_exp >= min_exp:
                points.append(f"Meets the required experience threshold with approximately **{cand_exp:g} years** of industry exposure (Target: {min_exp:g} yrs).")
            elif cand_exp > 0:
                points.append(f"Demonstrates **{cand_exp:g} years** of experience, slightly below the target of {min_exp:g} years.")
            else:
                points.append("Experience duration not explicitly stated; evaluated based on project scope and skill breadth.")

        # 2. Skill alignment
        if matched_skills:
            top_matched = ", ".join(f"`{s}`" for s in matched_skills[:6])
            points.append(f"Demonstrates proven capability in essential competencies: {top_matched}.")
        else:
            points.append("Limited direct overlap with explicit mandatory technical keywords.")

        # 3. Missing skills / gaps
        if missing_skills:
            top_missing = ", ".join(f"`{s}`" for s in missing_skills[:5])
            points.append(f"Key skill gaps to verify during screening: {top_missing}.")
        else:
            points.append("Comprehensive skill alignment with zero major mandatory competency gaps.")

        # 4. Contextual summary
        summary = (
            f"**{name}** achieved an overall match of **{score}%** against the **{jd_title}** position. "
            f"The candidate has a semantic contextual relevance of **{semantic}%** and a technical skill match of **{skill_score}%**.\n\n"
            + "\n".join(f"- {pt}" for pt in points)
        )

        return summary

    @classmethod
    def generate_llm_insights(
        cls,
        candidate: Dict[str, Any],
        jd_text: str,
        api_key: Optional[str] = None
    ) -> Optional[str]:
        """
        Optional GenAI enhancement using Google Gemini or OpenAI if API key is provided.
        Falls back seamlessly to local rationale if key is absent.
        """
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            return None

        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            You are an expert HR Talent Acquisition Specialist. Evaluate this candidate against the job description.
            
            Job Description:
            {jd_text[:1500]}
            
            Candidate Profile:
            Name: {candidate.get('candidate_name')}
            Experience: {candidate.get('experience_years')} years
            Skills: {', '.join(candidate.get('candidate_skills', []))}
            Matched Skills: {', '.join(candidate.get('matched_skills', []))}
            Missing Skills: {', '.join(candidate.get('missing_skills', []))}
            Match Score: {candidate.get('composite_score')}%
            
            Provide a 3-sentence executive hiring recommendation:
            1. Why this candidate was ranked here.
            2. Top 2 specific strengths.
            3. 1 key area to probe in the technical interview.
            """
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return None
