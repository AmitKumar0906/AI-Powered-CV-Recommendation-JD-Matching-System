"""
generate_samples.py: Creates realistic sample PDF resumes and Job Descriptions for instant testing.
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_pdf_resume(filepath: str, name: str, title: str, contact: str, summary: str, skills: str, experience: list, education: str):
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'HeaderName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B')
    )
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB')
    )
    contact_style = ParagraphStyle(
        'HeaderContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B')
    )
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    story = []
    # Header
    story.append(Paragraph(name, header_style))
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(contact, contact_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_title))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 10))

    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_title))
    story.append(Paragraph(skills, body_style))
    story.append(Spacer(1, 10))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_title))
    for exp_title, exp_desc in experience:
        story.append(Paragraph(f"<b>{exp_title}</b>", body_style))
        story.append(Paragraph(exp_desc, body_style))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 6))

    # Education
    story.append(Paragraph("EDUCATION", section_title))
    story.append(Paragraph(education, body_style))

    doc.build(story)


def generate_all_samples():
    resume_dir = os.path.join("data", "sample_resumes")
    jd_dir = os.path.join("data", "sample_jds")
    
    # Clean previous files to prevent orphaned files
    if os.path.exists(jd_dir):
        shutil.rmtree(jd_dir)
    if os.path.exists(resume_dir):
        shutil.rmtree(resume_dir)

    os.makedirs(resume_dir, exist_ok=True)
    os.makedirs(jd_dir, exist_ok=True)

    # 1. Comprehensive Sample Job Descriptions
    jds = {
        "01_Machine_Learning_Engineer.txt": """Machine Learning Engineer
Location: Hybrid | Experience: 4+ years of experience

About the Role:
We are looking for an experienced Machine Learning Engineer to design, build, and deploy production ML models and deep learning pipelines.

Key Requirements:
- 4+ years of hands-on experience in Machine Learning and Deep Learning.
- Strong proficiency in Python, PyTorch, TensorFlow, and Scikit-Learn.
- Experience building scalable training pipelines, MLOps, and model deployment using Docker and SQL.
- Strong understanding of algorithms, data structures, and mathematical foundations.
- Bachelor's or Master's degree in Computer Science (B.Tech, M.Tech, MS).
""",
        "02_Generative_AI_Engineer.txt": """Generative AI & LLM Engineer
Location: Remote | Experience: 3+ years of experience

About the Role:
We are seeking a Generative AI & LLM Engineer to build state-of-the-art enterprise AI applications leveraging Large Language Models, RAG, and agentic workflows.

Key Requirements:
- 3+ years of experience in NLP, Generative AI, and Transformer architectures.
- Hands-on expertise with LLMs, RAG, LangChain, LlamaIndex, BERT, and Transformers.
- Proficiency in Python, PyTorch, Scikit-Learn, and vector search (FAISS).
- Experience fine-tuning open-source models and prompt engineering.
- Bachelor's or Master's degree in AI, Data Science, or Computer Science.
""",
        "03_Data_Scientist.txt": """Data Scientist & Analytics Specialist
Location: Hybrid | Experience: 3+ years of experience

About the Role:
Looking for a Data Scientist to extract actionable insights, build predictive statistical models, and collaborate with product teams.

Key Requirements:
- 3+ years of professional experience in Data Science and Data Analysis.
- Strong proficiency in Python, SQL, Pandas, NumPy, and Scikit-Learn.
- Experience with data visualization (Matplotlib, Seaborn, Tableau) and exploratory analysis.
- Proven track record with machine learning classification, regression, and clustering.
- B.Tech, M.S., or equivalent quantitative degree.
""",
        "04_Senior_Full_Stack_Developer.txt": """Senior Full Stack Developer
Location: Remote | Experience: 3+ years of experience

About the Role:
We are seeking a talented Full Stack Developer to build modern web applications and robust microservices.

Key Requirements:
- 3+ years of experience in modern web development.
- Strong proficiency in React, TypeScript, JavaScript, Node.js, and Express.
- Experience with databases such as PostgreSQL and MongoDB.
- Experience building REST APIs, GraphQL, and microservices.
- Proficiency with Git, Docker, and CI/CD pipelines.
- Bachelor's degree (B.Tech or B.S.) in Computer Science.
""",
        "05_Cloud_DevOps_Architect.txt": """Cloud DevOps & Infrastructure Architect
Location: On-site | Experience: 5+ years of experience

About the Role:
Looking for a Senior DevOps Engineer to lead cloud infrastructure modernization, container orchestration, and CI/CD automation.

Key Requirements:
- 5+ years of experience in DevOps and Cloud Infrastructure.
- Deep expertise in AWS (Amazon Web Services), Docker, and Kubernetes (K8s).
- Strong hands-on experience with Terraform, Ansible, Jenkins, and Linux.
- Proficiency in Python or Bash scripting.
- Experience with monitoring systems like Prometheus and Grafana.
""",
        "06_Backend_Python_Developer.txt": """Senior Backend Python Developer
Location: Remote | Experience: 4+ years of experience

About the Role:
Seeking a Senior Backend Engineer to architect high-throughput microservices and APIs using modern Python frameworks.

Key Requirements:
- 4+ years of professional backend software engineering experience.
- Strong expertise in Python, FastAPI, Django, and Flask.
- Deep knowledge of relational and NoSQL databases: PostgreSQL, Redis, MySQL.
- Experience with Docker, microservices, system design, and REST APIs.
- Version control proficiency with Git and automated unit testing (Pytest).
""",
        "07_Frontend_React_Developer.txt": """Senior Frontend React Engineer
Location: Hybrid | Experience: 3+ years of experience

About the Role:
We are looking for a Senior Frontend Engineer passionate about crafting beautiful, high-performance web experiences.

Key Requirements:
- 3+ years of frontend development experience.
- Deep expertise in React, Next.js, TypeScript, and modern JavaScript.
- Proficiency in HTML5, CSS3, Tailwind, and responsive UI design.
- Experience integrating REST APIs and GraphQL.
- Strong understanding of web performance, Git, and component-driven architecture.
""",
        "08_Digital_Marketing_Specialist.txt": """Digital Marketing & Growth Manager
Location: On-site | Experience: 4+ years of experience

About the Role:
Seeking an experienced Digital Marketing Specialist to lead organic search optimization, content strategy, and multi-channel acquisition funnels.

Key Requirements:
- 4+ years in digital marketing, growth strategy, and SEO.
- Expertise in Google Analytics, content marketing, and copywriting.
- Experience managing social media campaigns and email marketing automation.
- Bachelor's degree in Marketing, Communications, or Business.
"""
    }

    for filename, content in jds.items():
        with open(os.path.join(jd_dir, filename), "w", encoding="utf-8") as f:
            f.write(content.strip())

    # 2. Comprehensive Candidate Pool (8 Diverse Resumes)
    candidates = [
        {
            "filename": "01_Alex_Rivera_ML_Engineer.pdf",
            "name": "Alex Rivera",
            "title": "Lead Machine Learning Engineer",
            "contact": "alex.rivera@email.com | +1 (555) 234-5678 | San Francisco, CA | github.com/alexrivera",
            "summary": "Accomplished Machine Learning Engineer with 5+ years of experience building, deploying, and optimizing predictive ML pipelines, deep learning architectures, and LLM systems at scale.",
            "skills": "Python, Machine Learning, Deep Learning, PyTorch, TensorFlow, Scikit-learn, NLP, Transformers, LLM, Pandas, NumPy, SQL, Docker, Git",
            "experience": [
                ("Senior ML Engineer - Vertex AI Labs (2021 - Present | 3 years)", "Architected deep learning pipelines improving model convergence by 35%. Deployed PyTorch models on Docker containers serving 5M+ daily requests."),
                ("Machine Learning Engineer - DataPulse Inc. (2019 - 2021 | 2 years)", "Engineered predictive machine learning models using Scikit-Learn and Pandas. Built end-to-end automated training workflows using SQL and Python.")
            ],
            "education": "M.Tech in Computer Science & Artificial Intelligence, Stanford University (2019)"
        },
        {
            "filename": "02_Priya_Sharma_GenAI_Specialist.pdf",
            "name": "Priya Sharma",
            "title": "Generative AI & NLP Specialist",
            "contact": "priya.sharma@email.com | +91 98765 43210 | Bangalore, India | linkedin.com/in/priyasharma",
            "summary": "Generative AI Specialist with over 3.5 years of experience specializing in Large Language Models, RAG architectures, LangChain, transformer models, and semantic search.",
            "skills": "Python, GenAI, Generative AI, LLM, RAG, LangChain, Transformers, BERT, NLP, FAISS, PyTorch, Scikit-learn, Pandas, SQL",
            "experience": [
                ("GenAI Research Engineer - AI Innovations Ltd (2022 - Present | 2.5 years)", "Engineered enterprise RAG pipelines using LangChain, FAISS, and custom LLM prompts. Fine-tuned open-source transformer models reducing retrieval hallucination by 40%."),
                ("NLP Data Scientist - InfoMetrics (2021 - 2022 | 1 year)", "Analyzed multi-terabyte datasets using Python and Pandas. Developed custom NLP tokenizers and sentiment analysis models with BERT.")
            ],
            "education": "B.Tech in Computer Science, IIT Madras (2021)"
        },
        {
            "filename": "03_Daniel_Kim_FullStack_Developer.pdf",
            "name": "Daniel Kim",
            "title": "Senior Full Stack Web Developer",
            "contact": "daniel.kim@email.com | +1 (555) 876-5432 | Austin, TX | github.com/danielkim",
            "summary": "Full Stack Software Engineer with 4+ years of experience designing robust frontend architectures with React and TypeScript and scalable backend APIs with Node.js and PostgreSQL.",
            "skills": "React, TypeScript, JavaScript, Node.js, Express, HTML, CSS, Tailwind, PostgreSQL, MongoDB, REST API, Docker, Git, CI/CD",
            "experience": [
                ("Senior Web Developer - CloudStack Technologies (2022 - Present | 2.5 years)", "Spearheaded frontend redesign in React and TypeScript, increasing user session duration by 35%. Built secure RESTful microservices in Node.js and Express."),
                ("Full Stack Engineer - TechFlow Solutions (2020 - 2022 | 2 years)", "Developed responsive web interfaces using React, JavaScript, and Tailwind. Optimized PostgreSQL database queries reducing API latency by 40%.")
            ],
            "education": "Bachelor of Science in Software Engineering, University of Texas (2020)"
        },
        {
            "filename": "04_Elena_Rostova_DevOps_Engineer.pdf",
            "name": "Elena Rostova",
            "title": "Cloud Architect & Senior DevOps Engineer",
            "contact": "elena.rostova@email.com | +1 (555) 345-6789 | Seattle, WA | github.com/erostova",
            "summary": "DevOps Engineer with 6+ years of experience automating enterprise cloud infrastructure across AWS, designing Kubernetes clusters, and setting up robust CI/CD deployment pipelines.",
            "skills": "AWS, Kubernetes, Docker, Terraform, Ansible, Jenkins, CI/CD, Linux, Python, Bash, Prometheus, Grafana, Git",
            "experience": [
                ("Lead DevOps Engineer - SkyHigh Cloud Systems (2021 - Present | 3.5 years)", "Engineered multi-region Kubernetes clusters on AWS managing 100+ microservices. Reduced deployment downtime by 99% with automated Jenkins and GitHub Actions pipelines."),
                ("Cloud Systems Engineer - CoreNet Networks (2018 - 2021 | 3 years)", "Implemented Infrastructure as Code using Terraform and Ansible. Automated server provisioning and Linux environment hardening.")
            ],
            "education": "B.S. in Computer Engineering, University of Washington (2018)"
        },
        {
            "filename": "05_Marcus_Vance_Backend_Python.pdf",
            "name": "Marcus Vance",
            "title": "Senior Backend Python Engineer",
            "contact": "marcus.vance@email.com | +1 (555) 678-1234 | Chicago, IL | github.com/marcusvance",
            "summary": "Backend Python Developer with 4.5 years of experience building high-performance asynchronous microservices with FastAPI, Django, PostgreSQL, and Redis.",
            "skills": "Python, FastAPI, Django, Flask, PostgreSQL, Redis, MySQL, Docker, REST API, Microservices, Git, Pytest, SQL",
            "experience": [
                ("Lead Backend Developer - StreamSync Inc (2022 - Present | 2.5 years)", "Built asynchronous microservices in FastAPI and PostgreSQL serving 20,000 requests/sec. Integrated Redis caching and automated Pytest workflows in Docker."),
                ("Python Backend Engineer - DataNexus (2020 - 2022 | 2 years)", "Developed scalable REST APIs using Django and PostgreSQL. Designed database indexing strategies reducing query times by 50%.")
            ],
            "education": "B.Tech in Computer Science, University of Illinois (2020)"
        },
        {
            "filename": "06_Aisha_Khan_Frontend_React.pdf",
            "name": "Aisha Khan",
            "title": "Senior Frontend React Developer",
            "contact": "aisha.khan@email.com | +44 20 7946 0912 | London, UK | github.com/aishakhan",
            "summary": "Frontend Specialist with 3.5 years of experience creating highly accessible, pixel-perfect user interfaces using React, Next.js, TypeScript, and modern CSS/Tailwind.",
            "skills": "React, Next.js, TypeScript, JavaScript, HTML, CSS, Tailwind, GraphQL, REST API, Git, Webpack, Responsive Design",
            "experience": [
                ("Senior Frontend Engineer - FinTech Visuals (2022 - Present | 2.5 years)", "Designed and maintained complex financial analytics dashboards in Next.js and React. Implemented responsive Tailwind UI design and optimized client-side bundle size."),
                ("Frontend Developer - PixelStudio UK (2021 - 2022 | 1 year)", "Built modular component libraries in React and TypeScript. Collaborated with UI/UX designers to translate Figma mockups into accessible web apps.")
            ],
            "education": "B.Sc in Computing & Interactive Media, University of Manchester (2021)"
        },
        {
            "filename": "07_Rohan_Mehta_Junior_Developer.pdf",
            "name": "Rohan Mehta",
            "title": "Junior Python & Web Developer",
            "contact": "rohan.mehta@email.com | +91 91234 56789 | Mumbai, India | github.com/rohanm",
            "summary": "Enthusiastic Junior Software Developer with 1.5 years of experience in Python backend development, Flask APIs, and relational databases.",
            "skills": "Python, Flask, JavaScript, HTML, CSS, SQL, MySQL, Git, Data Structures",
            "experience": [
                ("Junior Python Developer - Apex Digital (2023 - Present | 1.5 years)", "Developed REST APIs using Python and Flask. Maintained SQL databases and implemented unit tests with Pytest.")
            ],
            "education": "B.Tech in Information Technology, Mumbai University (2023)"
        },
        {
            "filename": "08_Sarah_Jenkins_Marketing_Lead.pdf",
            "name": "Sarah Jenkins",
            "title": "Digital Marketing & Growth Strategist",
            "contact": "sarah.jenkins@email.com | +1 (555) 456-7890 | Chicago, IL",
            "summary": "Strategic Marketing Specialist with 5+ years of experience directing social media campaigns, SEO optimization, brand narrative, and content marketing.",
            "skills": "Digital Marketing, SEO, Content Strategy, Google Analytics, Social Media, Copywriting, Email Campaigns, Brand Strategy",
            "experience": [
                ("Marketing Manager - GrowthBrand Media (2021 - Present | 3 years)", "Managed multi-channel digital campaigns generating 40% user acquisition growth. Directed content strategy and organic search SEO rankings."),
                ("Content Strategist - Pulse Agency (2019 - 2021 | 2 years)", "Authored brand copy and executed email marketing funnels for B2B tech clients.")
            ],
            "education": "Bachelor of Arts in Communications & Marketing, Northwestern University (2019)"
        }
    ]

    for cand in candidates:
        pdf_path = os.path.join(resume_dir, cand["filename"])
        create_pdf_resume(
            pdf_path,
            cand["name"],
            cand["title"],
            cand["contact"],
            cand["summary"],
            cand["skills"],
            cand["experience"],
            cand["education"]
        )

    print(f"Generated {len(jds)} target Job Descriptions and {len(candidates)} realistic PDF resumes successfully.")


if __name__ == "__main__":
    generate_all_samples()
