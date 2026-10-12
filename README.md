# 🎯 AI Talent Matcher: CV Recommendation System & CV Parsing (JD Matching)

> **Cognizant SOA Short Listed Use Case #4**  
> **Mentor:** Satarupa Subhra Biswal  
> **Type:** Classification / Recommender / GenAI

---

## 📌 Project Overview
Recruiters manually screen hundreds of resumes against job descriptions, a process that is time-consuming, prone to human bias, and inconsistent across varied resume templates.

**AI Talent Matcher** is an end-to-end Machine Learning and GenAI-powered system that:
1. **Parses CVs and Job Descriptions** into structured profiles (Name, Email, Phone, Skills, Experience, Education).
2. **Computes Semantic Match Scores** using dense contextual sentence embeddings (`all-MiniLM-L6-v2`).
3. **Applies Hybrid Ranking** combining deep semantic relevance, required skill overlap, and experience fit.
4. **Delivers Explainable AI (XAI)** by displaying matched skills (green badges), missing critical skills (red badges), and executive shortlisting rationale.
5. **Provides an Interactive Web Dashboard** built with Streamlit for one-click candidate ranking and CSV shortlisting export.

---

## 🚀 How to Run in VS Code (Quickstart)

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File** > **Open Folder...** and select this directory:
   `c:\Users\Amit Singh\Desktop\NPN project`

### Step 2: Run the Web Dashboard
Open the integrated terminal in VS Code (`Ctrl + ~` or **Terminal > New Terminal**) and execute:

```powershell
streamlit run app.py
```

The browser will automatically open at `http://localhost:8501`.

---

## 🧪 Testing & Verification
You can run the automated pipeline test anytime from the terminal:

```powershell
python test_pipeline.py
```

This verifies that:
- PDF resumes are parsed without data loss.
- The `SentenceTransformer` model embeds text accurately.
- Machine Learning candidates rank at the top for Data Science roles, and non-technical profiles rank at the bottom.

---

## 📂 Project Architecture & Directory Structure

```text
NPN project/
├── app.py                   # Streamlit Recruiter Dashboard UI
├── test_pipeline.py         # Automated end-to-end verification script
├── generate_samples.py      # Generates realistic sample PDF resumes & JDs
├── requirements.txt         # Project dependencies
├── README.md                # Documentation & mentor presentation guide
│
├── src/
│   ├── __init__.py
│   ├── parser.py            # PDF/DOCX/TXT text extraction & structured parsing
│   ├── matcher.py           # Embeddings, Cosine Similarity & Hybrid scoring engine
│   ├── explainer.py         # Explainable AI rationale & GenAI recommendations
│   └── utils.py             # Domain skill taxonomy & regex entity patterns
│
└── data/
    ├── sample_resumes/      # 6 Realistic PDF resumes (ML, NLP, Full Stack, DevOps, Junior, Marketing)
    └── sample_jds/          # 3 Pre-configured Job Descriptions (Data Science, Web Dev, Cloud/DevOps)
```

---

## 🧠 Scoring Methodology (Hybrid Recommendation)

Candidate ranking uses a composite weighted scoring formula:

$$\text{Final Score} = w_1 \cdot \text{Semantic Match} + w_2 \cdot \text{Skill Overlap} + w_3 \cdot \text{Experience Fit}$$

| Component | Default Weight | Method | Purpose |
|---|---|---|---|
| **Semantic Match** | 50% | Cosine similarity on `all-MiniLM-L6-v2` embeddings | Captures overall contextual relevance, synonyms, and domain intent. |
| **Skill Match** | 35% | Jaccard overlap against canonical skill taxonomy | Ensures mandatory technical qualifications are met. |
| **Experience Fit** | 15% | Heuristic experience ratio against JD requirements | Rewards candidates meeting seniority thresholds. |

*Weights are fully customizable in real-time via the sidebar sliders in the Streamlit app.*

---

## 🎤 Key Points to Present to Your Mentor

1. **Solves the Core Problem:** Eliminates manual resume screening fatigue and standardizes evaluation criteria across heterogeneous resume formats.
2. **Hybrid Advantage:** Unlike pure keyword matching (which misses synonyms) or pure semantic search (which can hallucinate relevance), the hybrid approach guarantees that mandatory technical skills are verified.
3. **Zero Black-Box Obscurity:** The recruiter dashboard explicitly shows *why* a candidate was shortlisted, highlighting exact matching competencies and missing prerequisite skills.
4. **Production-Ready & Offline Capable:** Runs locally on CPU with millisecond latency without requiring paid API tokens. Supports optional Gemini LLM integration for extra conversational recruiter commentary.
