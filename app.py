"""
app.py: Streamlit Recruiter Dashboard for CV Recommendation System & Parsing (JD Matching).
"""

import io
import os
import pandas as pd
import streamlit as st

from src.explainer import RecommendationExplainer
from src.matcher import CandidateMatcher
from src.parser import DocumentParser

# Page configuration
st.set_page_config(
    page_title="AI Talent Matcher | CV Recommendation & Parsing",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .skill-tag-matched {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.18);
        color: #22c55e;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 14px;
        margin: 3px;
        border: 1px solid rgba(34, 197, 94, 0.45);
    }
    .skill-tag-missing {
        display: inline-block;
        background-color: rgba(239, 68, 68, 0.18);
        color: #ef4444;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 14px;
        margin: 3px;
        border: 1px solid rgba(239, 68, 68, 0.45);
    }
    .skill-tag-neutral {
        display: inline-block;
        background-color: rgba(148, 163, 184, 0.18);
        color: #94a3b8;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 4px 12px;
        border-radius: 14px;
        margin: 3px;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }
    .candidate-card {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
        background-color: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)


def load_sample_jds():
    jd_dir = os.path.join("data", "sample_jds")
    jds = {}
    if os.path.exists(jd_dir):
        for f in sorted(os.listdir(jd_dir)):
            if f.endswith(".txt"):
                display_name = f.replace(".txt", "").replace("_", " ")[3:]
                with open(os.path.join(jd_dir, f), "r", encoding="utf-8") as file:
                    jds[display_name] = file.read()
    return jds


def load_sample_resumes(category: str = "professional"):
    if category == "student":
        res_dir = os.path.join("data", "student_resumes")
    else:
        res_dir = os.path.join("data", "sample_resumes")
    resumes = []
    if os.path.exists(res_dir):
        for f in sorted(os.listdir(res_dir)):
            if f.endswith(".pdf"):
                full_path = os.path.join(res_dir, f)
                resumes.append(full_path)
    return resumes


def load_kaggle_categories():
    kaggle_dir = os.path.join("data", "data")
    if not os.path.exists(kaggle_dir):
        return []
    return sorted([d for d in os.listdir(kaggle_dir) if os.path.isdir(os.path.join(kaggle_dir, d))])


def load_kaggle_resumes(category: str):
    cdir = os.path.join("data", "data", category)
    if not os.path.exists(cdir):
        return []
    return [os.path.join(cdir, f) for f in sorted(os.listdir(cdir)) if f.endswith(".pdf")]


# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/resume.png", width=64)
    st.title("Screening Engine")
    st.caption("CV Recommendation & Parsing System")
    st.divider()

    st.subheader("⚙️ Scoring Weights")
    st.caption("Adjust the balance of the recommendation algorithm:")
    w_semantic = st.slider("Dense Semantic Match", min_value=0.1, max_value=0.8, value=0.50, step=0.05)
    w_skills = st.slider("Direct Skill Overlap", min_value=0.1, max_value=0.8, value=0.35, step=0.05)
    w_experience = st.slider("Experience Alignment", min_value=0.0, max_value=0.5, value=0.15, step=0.05)

    st.divider()
    st.subheader("🎯 Shortlisting Filter")
    score_threshold = st.slider("Minimum Match Threshold (%)", min_value=30, max_value=90, value=50, step=5)

    st.divider()
    with st.expander("🤖 Optional GenAI LLM API Key"):
        gemini_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIzaSy...")
        st.caption("Offline explainability works automatically even without an API key.")


# --- MAIN HEADER ---
st.title("🎯 AI Talent Matcher")
st.markdown("### Intelligent CV Recommendation & JD Matching System")
st.markdown("Automated candidate ranking using **Sentence Transformers**, **Entity Extraction**, and **Explainable AI**.")

tab_run, tab_about = st.tabs(["🚀 Screening & Recommendation", "ℹ️ System Architecture & Guide"])

with tab_run:
    col_jd, col_res = st.columns([1, 1], gap="large")

    # --- SECTION 1: JOB DESCRIPTION ---
    with col_jd:
        st.subheader("1. Job Description (JD)")
        jd_options = load_sample_jds()

        jd_source = st.radio(
            "Select JD Source:",
            ["Use Pre-loaded Sample Role", "Paste or Type Custom JD"],
            horizontal=True
        )

        if jd_source == "Use Pre-loaded Sample Role" and jd_options:
            selected_jd_name = st.selectbox(f"Choose Target Job Role ({len(jd_options)} Available):", list(jd_options.keys()))
            jd_text_input = st.text_area("Job Description Content:", jd_options[selected_jd_name], height=240)
            with st.expander(f"📚 Catalog of All {len(jd_options)} Pre-loaded Job Roles", expanded=False):
                jd_list = [{"#": i, "Job Role Title": k} for i, k in enumerate(jd_options.keys(), 1)]
                st.dataframe(pd.DataFrame(jd_list), hide_index=True, use_container_width=True)
        else:
            jd_text_input = st.text_area(
                "Job Description Content:",
                placeholder="Paste the Job Description here (including role title, required skills, and experience)...",
                height=280
            )

        # Parse JD preview
        if jd_text_input.strip():
            parsed_jd = DocumentParser.parse_job_description(jd_text_input)
            with st.expander("📋 View Parsed JD Requirements", expanded=True):
                st.write(f"**Target Role:** {parsed_jd['title']}")
                st.write(f"**Min. Experience Required:** {parsed_jd['min_experience_years']} years" if parsed_jd['min_experience_years'] > 0 else "**Min. Experience:** Flexible")
                st.write("**Extracted Required Skills:**")
                if parsed_jd["required_skills"]:
                    tags = "".join(f'<span class="skill-tag-neutral">{s}</span>' for s in parsed_jd["required_skills"])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.caption("No explicit taxonomy skills detected; relying on deep semantic matching.")
        else:
            parsed_jd = None

    # --- SECTION 2: RESUME POOL ---
    with col_res:
        st.subheader("2. Candidate Resumes")
        kaggle_cats = load_kaggle_categories()
        has_kaggle = len(kaggle_cats) > 0

        pool_options = []
        if has_kaggle:
            pool_options.append("Kaggle Dataset (2,484 Resumes in 24 Domains)")
        pool_options.extend(["Experienced Professionals (8 Resumes)", "Upload Custom Files (PDF / DOCX)"])

        resume_source = st.radio(
            "Select Candidate Pool:",
            pool_options,
            horizontal=True
        )

        resumes_to_process = []
        if resume_source.startswith("Kaggle Dataset"):
            default_idx = kaggle_cats.index("INFORMATION-TECHNOLOGY") if "INFORMATION-TECHNOLOGY" in kaggle_cats else 0
            selected_domain = st.selectbox(f"Choose Resume Domain ({len(kaggle_cats)} Available):", kaggle_cats, index=default_idx)
            domain_resumes = load_kaggle_resumes(selected_domain)
            st.info(f"Loaded **{len(domain_resumes)} resumes** from `{selected_domain}` domain.")

            k_count = st.slider(
                "How many resumes to screen from this domain?",
                min_value=1,
                max_value=len(domain_resumes),
                value=min(len(domain_resumes), 10),
                step=1,
                help=f"Select batch size (up to all {len(domain_resumes)} resumes in this domain)."
            )
            resumes_to_process = domain_resumes[:k_count]
            st.caption(f"✅ Screening first **{len(resumes_to_process)} of {len(domain_resumes)}** resumes.")

            with st.expander(f"📄 Inspect {selected_domain} Resumes ({len(domain_resumes)} Files)", expanded=False):
                k_list = [{"#": i, "Resume File": os.path.basename(p)} for i, p in enumerate(domain_resumes, 1)]
                st.dataframe(pd.DataFrame(k_list), hide_index=True, use_container_width=True)

        elif resume_source.startswith("Experienced Professionals"):
            sample_resumes = load_sample_resumes(category="professional")
            st.info(f"Loaded **{len(sample_resumes)} verified experienced professionals (AI/ML, Full Stack, Cloud/DevOps, Marketing)**.")
            
            bundled_map = {os.path.basename(p).replace(".pdf", "").replace("_", " ")[3:]: p for p in sample_resumes}
            candidate_names = list(bundled_map.keys())

            sel_mode = st.radio(
                "Choose Resume Selection Method:",
                ["All Resumes", "Pick Specific Candidates", "Select by Count (Slider)"],
                horizontal=True,
                key="bundled_sel_mode"
            )

            if sel_mode == "All Resumes":
                resumes_to_process = sample_resumes
                st.caption(f"✅ Selected all {len(resumes_to_process)} candidates for screening.")
            elif sel_mode == "Pick Specific Candidates":
                chosen_names = st.multiselect(
                    "Pick candidates to include in screening:",
                    options=candidate_names,
                    default=candidate_names[:4],
                    help="Select or deselect any specific candidate."
                )
                resumes_to_process = [bundled_map[name] for name in chosen_names]
                st.caption(f"✅ Selected **{len(resumes_to_process)} of {len(sample_resumes)}** candidates.")
            else:
                num_resumes = st.slider(
                    "How many resumes to screen?",
                    min_value=1,
                    max_value=len(sample_resumes),
                    value=len(sample_resumes),
                    step=1
                )
                resumes_to_process = sample_resumes[:num_resumes]
                st.caption(f"✅ Screening first **{num_resumes} of {len(sample_resumes)}** resumes.")

            with st.expander(f"📄 Inspect All Loaded Resumes ({len(sample_resumes)} Candidates)", expanded=False):
                res_list = []
                for idx, rpath in enumerate(sample_resumes, 1):
                    fname = os.path.basename(rpath)
                    clean_name = fname.replace(".pdf", "").replace("_", " ")[3:]
                    res_list.append({"#": idx, "Candidate Profile": clean_name, "File": fname})
                st.dataframe(pd.DataFrame(res_list), hide_index=True, use_container_width=True)
        else:
            uploaded_files = st.file_uploader(
                "Upload Resume Files (Multiple allowed)",
                type=["pdf", "docx", "txt"],
                accept_multiple_files=True
            )
            if uploaded_files:
                total_uploaded = len(uploaded_files)
                st.success(f"{total_uploaded} resumes uploaded.")

                custom_sel_mode = st.radio(
                    "Choose How Many Uploaded Resumes to Screen:",
                    [f"All Uploaded ({total_uploaded})", "Pick Specific Files", "Select by Count (Slider)"],
                    horizontal=True,
                    key="custom_sel_mode"
                )

                if custom_sel_mode.startswith("All Uploaded"):
                    resumes_to_process = uploaded_files
                    st.caption(f"✅ Selected all {len(resumes_to_process)} uploaded files.")
                elif custom_sel_mode == "Pick Specific Files":
                    file_names = [f.name for f in uploaded_files]
                    chosen_files = st.multiselect(
                        "Select specific uploaded files:",
                        options=file_names,
                        default=file_names
                    )
                    resumes_to_process = [f for f in uploaded_files if f.name in chosen_files]
                    st.caption(f"✅ Selected **{len(resumes_to_process)} of {total_uploaded}** uploaded files.")
                else:
                    num_custom = st.slider(
                        "How many uploaded resumes to screen?",
                        min_value=1,
                        max_value=total_uploaded,
                        value=min(total_uploaded, 5),
                        step=1
                    )
                    resumes_to_process = uploaded_files[:num_custom]
                    st.caption(f"✅ Screening first **{len(resumes_to_process)} of {total_uploaded}** uploaded resumes.")
            else:
                resumes_to_process = []

    st.divider()

    # --- SECTION 3: SCREENING ACTION ---
    col_action, col_spacer = st.columns([1, 2])
    with col_action:
        run_screening = st.button("🚀 Screen & Rank Candidates", type="primary", use_container_width=True)

    if run_screening:
        if not jd_text_input.strip():
            st.error("Please provide a Job Description to proceed.")
        elif not resumes_to_process:
            st.error("Please upload or select at least one resume.")
        else:
            with st.spinner("Parsing resumes and computing semantic match embeddings..."):
                # 1. Parse all resumes
                parsed_resumes = []
                for item in resumes_to_process:
                    if isinstance(item, str):
                        parsed = DocumentParser.parse_resume(item)
                    else:
                        parsed = DocumentParser.parse_resume(io.BytesIO(item.getvalue()), filename=item.name)
                    parsed_resumes.append(parsed)

                # 2. Rank candidates
                ranked_candidates = CandidateMatcher.rank_candidates(
                    parsed_resumes=parsed_resumes,
                    parsed_jd=parsed_jd,
                    semantic_weight=w_semantic,
                    skill_weight=w_skills,
                    experience_weight=w_experience
                )

                st.session_state["results"] = ranked_candidates
                st.session_state["parsed_jd"] = parsed_jd

    # --- SECTION 4: RESULTS DASHBOARD ---
    if "results" in st.session_state and st.session_state["results"]:
        results = st.session_state["results"]
        active_jd = st.session_state["parsed_jd"]

        st.subheader("📊 Candidate Recommendation Leaderboard")

        # Top KPI Metrics
        total_candidates = len(results)
        shortlisted = [c for c in results if c["composite_score"] >= score_threshold]
        top_score = results[0]["composite_score"] if results else 0
        avg_score = round(sum(c["composite_score"] for c in results) / total_candidates, 1)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Screened", total_candidates)
        m2.metric(f"Shortlisted (≥{score_threshold}%)", f"{len(shortlisted)} ({round(len(shortlisted)/total_candidates*100)}%)")
        m3.metric("Top Match Score", f"{top_score}%")
        m4.metric("Average Score", f"{avg_score}%")

        # Leaderboard Summary Table
        table_rows = []
        for c in results:
            verdict = RecommendationExplainer.get_verdict(c["composite_score"])
            table_rows.append({
                "Rank": f"#{c['rank']}",
                "Candidate Name": c["candidate_name"],
                "Match Score": f"{c['composite_score']}%",
                "Verdict": verdict["badge"],
                "Semantic Sim": f"{c['semantic_score']}%",
                "Skill Match": f"{c['skill_score']}%",
                "Exp (Yrs)": f"{c['experience_years']} yrs" if c['experience_years'] > 0 else "N/A",
                "Matched Skills Count": len(c["matched_skills"]),
                "Missing Skills Count": len(c["missing_skills"])
            })

        df_leaderboard = pd.DataFrame(table_rows)
        st.dataframe(df_leaderboard, use_container_width=True, hide_index=True)

        # Download Shortlist Button
        csv_data = df_leaderboard.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Candidate Shortlist (CSV)",
            data=csv_data,
            file_name="candidate_shortlist.csv",
            mime="text/csv"
        )

        st.divider()

        # Detailed Candidate Cards
        st.subheader("🔍 Deep-Dive Candidate Explainability")

        for cand in results:
            verdict = RecommendationExplainer.get_verdict(cand["composite_score"])
            is_above_threshold = cand["composite_score"] >= score_threshold

            with st.expander(
                f"Rank #{cand['rank']} — {cand['candidate_name']} ({cand['composite_score']}%) | {verdict['badge']}",
                expanded=(cand["rank"] == 1)
            ):
                c_left, c_right = st.columns([1, 2])

                with c_left:
                    st.write(f"**Contact:** `{cand['email']}` | `{cand['phone']}`")
                    st.write(f"**Filename:** `{cand['filename']}`")
                    st.write(f"**Experience:** {cand['experience_years']} years")
                    st.write(f"**Education:** {', '.join(cand['education']) if cand['education'] else 'Degree in record'}")

                    # Score Breakdown Progress Bars
                    st.write("**Score Breakdown:**")
                    st.caption(f"Composite Score: {cand['composite_score']}%")
                    st.progress(cand["composite_score"] / 100.0)

                    st.caption(f"Semantic Context: {cand['semantic_score']}%")
                    st.progress(cand["semantic_score"] / 100.0)

                    st.caption(f"Skill Match: {cand['skill_score']}%")
                    st.progress(cand["skill_score"] / 100.0)

                with c_right:
                    # Matched vs Missing Skills Badges
                    st.write("**✅ Skills Found in Candidate Resume:**")
                    if cand["matched_skills"]:
                        matched_html = "".join(f'<span class="skill-tag-matched">✓ {s}</span>' for s in cand["matched_skills"])
                        st.markdown(matched_html, unsafe_allow_html=True)
                    else:
                        st.write("None detected")

                    st.write("**⚠️ Skill Gaps (Required by JD, but Missing in Resume):**")
                    if cand["missing_skills"]:
                        missing_html = "".join(f'<span class="skill-tag-missing">✗ {s}</span>' for s in cand["missing_skills"])
                        st.markdown(missing_html, unsafe_allow_html=True)
                    else:
                        st.write("None — Full coverage!")

                    st.markdown("---")
                    st.write("**💡 AI Recommendation & Shortlisting Rationale:**")
                    rationale = RecommendationExplainer.generate_rationale(
                        candidate=cand,
                        jd_title=active_jd.get("title", "Position"),
                        min_exp=active_jd.get("min_experience_years", 0)
                    )
                    st.markdown(rationale)

                    # Optional LLM output if API key is provided
                    if gemini_key:
                        llm_insight = RecommendationExplainer.generate_llm_insights(cand, active_jd.get("raw_text", ""), api_key=gemini_key)
                        if llm_insight:
                            st.info(f"**Gemini AI Recruiter Note:**\n\n{llm_insight}")

with tab_about:
    st.subheader("System Architecture & Implementation Summary")
    st.markdown("""
    This project satisfies **Project 4: CV Recommendation System & CV Parsing (JD Matching)** for recruiter automation.

    ### 🛠️ Architecture Highlights:
    1. **Document Ingestion Layer:** Robust multi-format parsing (`.pdf`, `.docx`, `.txt`) using `pypdf` and `python-docx`.
    2. **Entity & Skill Extraction:** Domain-specific taxonomy extraction covering AI/ML, Cloud/DevOps, Full Stack, and Databases.
    3. **Semantic Recommendation Engine:**
       - Uses `sentence-transformers` (`all-MiniLM-L6-v2`) to capture context and intent beyond simple keyword search.
       - Vectorized Cosine Similarity between JD and resume profiles.
    4. **Hybrid Composite Scoring:**
       $$\\text{Final Score} = w_1 \\cdot \\text{Semantic} + w_2 \\cdot \\text{Skill Overlap} + w_3 \\cdot \\text{Experience Fit}$$
    5. **Explainable AI (XAI):**
       - Clear visual tags distinguishing matched capabilities (green) from skill gaps (red).
       - Recruiter justification report with zero black-box obscurity.
    """)
