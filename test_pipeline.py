"""
test_pipeline.py: Unit and pipeline verification test for parsing and recommendation.
"""

import os
from src.parser import DocumentParser
from src.matcher import CandidateMatcher
from src.explainer import RecommendationExplainer


def run_pipeline_test():
    print("=" * 60)
    print("RUNNING END-TO-END PIPELINE VERIFICATION")
    print("=" * 60)

    # 1. Load Machine Learning Engineer JD
    jd_path = os.path.join("data", "sample_jds", "01_Machine_Learning_Engineer.txt")
    assert os.path.exists(jd_path), f"JD file not found: {jd_path}"
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    parsed_jd = DocumentParser.parse_job_description(jd_text)
    print(f"Target JD Title: {parsed_jd['title']}")
    print(f"Required Skills ({len(parsed_jd['required_skills'])}): {', '.join(parsed_jd['required_skills'])}")
    print(f"Min Experience: {parsed_jd['min_experience_years']} years")
    print("-" * 60)

    # 2. Parse Resumes
    resume_dir = os.path.join("data", "sample_resumes")
    resume_files = [os.path.join(resume_dir, f) for f in sorted(os.listdir(resume_dir)) if f.endswith(".pdf")]
    print(f"Parsing {len(resume_files)} PDF resumes...")

    parsed_resumes = []
    for rpath in resume_files:
        parsed = DocumentParser.parse_resume(rpath)
        parsed_resumes.append(parsed)
        print(f"  - Parsed: {parsed['name']} ({len(parsed['skills'])} skills, {parsed['experience_years']} yrs exp)")

    print("-" * 60)
    print("Running Candidate Matcher & Embedding Model...")
    ranked = CandidateMatcher.rank_candidates(parsed_resumes, parsed_jd)

    print("\nFINAL LEADERBOARD RESULTS:")
    for cand in ranked:
        verdict = RecommendationExplainer.get_verdict(cand['composite_score'])
        print(f"Rank #{cand['rank']}: {cand['candidate_name']:<18} | Match: {cand['composite_score']:>5}% | Semantic: {cand['semantic_score']:>5}% | Skills: {cand['skill_score']:>5}% | Status: {verdict['status']}")

    # Assertions for sanity checking
    top_candidate = ranked[0]["candidate_name"]
    bottom_candidate = ranked[-1]["candidate_name"]

    print("\nVerification Checks:")
    print(f"  Top Candidate for ML Engineer role: {top_candidate}")
    print(f"  Lowest Candidate for ML Engineer role: {bottom_candidate}")

    assert "Alex Rivera" in top_candidate, "Expected Alex Rivera (ML Engineer) to rank #1"
    assert "Sarah Jenkins" in bottom_candidate, "Expected non-technical marketing candidate to rank at bottom"
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_pipeline_test()
