"""
generate_student_dataset.py: Creates realistic college student and fresher resumes (PDF) and internship JDs.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_pdf_student_resume(filepath: str, name: str, college: str, degree: str, contact: str, summary: str, skills: str, projects: list, education: str):
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
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )
    sub_style = ParagraphStyle(
        'HeaderSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
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
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155')
    )

    story = []
    # Header
    story.append(Paragraph(name, header_style))
    story.append(Paragraph(f"{degree} — {college}", sub_style))
    story.append(Paragraph(contact, contact_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    # Profile
    story.append(Paragraph("CAREER OBJECTIVE", section_title))
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 8))

    # Education
    story.append(Paragraph("EDUCATION", section_title))
    story.append(Paragraph(education, body_style))
    story.append(Spacer(1, 8))

    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_title))
    story.append(Paragraph(skills, body_style))
    story.append(Spacer(1, 8))

    # Academic & Internship Projects
    story.append(Paragraph("ACADEMIC PROJECTS & INTERNSHIPS", section_title))
    for p_title, p_desc in projects:
        story.append(Paragraph(f"<b>{p_title}</b>", body_style))
        story.append(Paragraph(p_desc, body_style))
        story.append(Spacer(1, 5))

    doc.build(story)


def generate_all_student_data():
    student_dir = os.path.join("data", "student_resumes")
    jd_dir = os.path.join("data", "sample_jds")
    os.makedirs(student_dir, exist_ok=True)
    os.makedirs(jd_dir, exist_ok=True)

    # 1. Add Campus & Internship Job Descriptions
    intern_jds = {
        "09_AI_Machine_Learning_Intern.txt": """AI & Machine Learning Graduate Intern
Location: Remote / Campus | Experience: 0 - 1 years (Fresher / Student)

About the Internship:
Looking for passionate final-year students or recent graduates with strong foundational knowledge in Machine Learning and Python to join our AI Research lab.

Key Requirements:
- Final year B.Tech, M.Tech, MCA, or M.Sc in Computer Science or Data Science.
- Strong knowledge of Python, NumPy, Pandas, Scikit-learn, and basic Deep Learning (PyTorch or TensorFlow).
- Hands-on experience with academic projects or hackathons involving NLP, Computer Vision, or ML algorithms.
- Solid understanding of data structures, algorithms, and SQL.
- Eagerness to learn Generative AI, LLMs, and model deployment.
""",
        "10_Software_Engineer_Intern.txt": """Software Engineer Intern (Full Stack / Web)
Location: Hybrid | Experience: 0 - 1 years (Fresher / Student)

About the Internship:
We are hiring Software Development Interns to build modern web interfaces and backend services for our product engineering team.

Key Requirements:
- Pursuing or completed Bachelor's degree (B.Tech, B.E., BCA) in Computer Science or IT.
- Proficiency in JavaScript, React, HTML5, CSS3, and Node.js.
- Basic knowledge of databases like PostgreSQL, MySQL, or MongoDB.
- Familiarity with Git version control and REST APIs.
- Strong problem-solving skills and ability to work in an agile team.
"""
    }

    for fname, content in intern_jds.items():
        with open(os.path.join(jd_dir, fname), "w", encoding="utf-8") as f:
            f.write(content.strip())

    # 2. Student & Fresher Resumes
    students = [
        {
            "filename": "01_Aarav_Sharma_AI_Student.pdf",
            "name": "Aarav Sharma",
            "college": "Delhi Technological University (DTU)",
            "degree": "B.Tech in Computer Science (4th Year)",
            "contact": "aarav.sharma@student.dtu.ac.in | +91 98111 22334 | New Delhi | github.com/aarav-ai",
            "summary": "Enthusiastic final year Computer Science student passionate about Machine Learning and AI. Experienced with Scikit-learn, PyTorch, and NLP through university research and hackathons.",
            "skills": "Python, Machine Learning, Deep Learning, PyTorch, Scikit-learn, Pandas, NumPy, SQL, Git, Data Structures, Algorithms",
            "education": "B.Tech in Computer Science (CGPA: 8.8/10), Expected May 2026",
            "projects": [
                ("Machine Learning Intern - TechStartup Delhi (Summer 2025 | 3 months)", "Implemented predictive customer churn model using Scikit-Learn and Pandas. Improved baseline recall by 18%."),
                ("Capstone Project: Autonomous Object Detection with PyTorch", "Trained a convolutional deep learning model for real-time video stream detection with 86% accuracy.")
            ]
        },
        {
            "filename": "02_Sneha_Patel_WebDev_Student.pdf",
            "name": "Sneha Patel",
            "college": "Vellore Institute of Technology (VIT)",
            "degree": "B.Tech in Information Technology (4th Year)",
            "contact": "sneha.patel@vitstudent.ac.in | +91 98222 33445 | Chennai | github.com/snehapatel-web",
            "summary": "Full stack web developer and aspiring software engineer with hands-on experience in React, JavaScript, Node.js, and MongoDB through college club projects.",
            "skills": "React, JavaScript, TypeScript, Node.js, Express, HTML, CSS, Tailwind, MongoDB, Git, REST API",
            "education": "B.Tech in Information Technology (CGPA: 8.6/10), Expected June 2026",
            "projects": [
                ("Campus Event Portal - MERN Stack", "Built responsive web application using React, Node.js, and MongoDB with JWT authentication used by 3,000+ students."),
                ("Web Development Intern - SoftSolutions (Summer 2025 | 2 months)", "Developed reusable React UI components and integrated RESTful endpoints.")
            ]
        },
        {
            "filename": "03_Ananya_Gupta_DataScience_Student.pdf",
            "name": "Ananya Gupta",
            "college": "BITS Pilani",
            "degree": "B.Tech in Artificial Intelligence & Data Science",
            "contact": "ananya.gupta@pilani.bits-pilani.ac.in | +91 98333 44556 | Pilani | github.com/ananyag-ds",
            "summary": "Final year undergraduate researcher focused on Natural Language Processing, GenAI, and transformer architectures. Completed internships in data science and text analysis.",
            "skills": "Python, NLP, GenAI, Transformers, Scikit-learn, Pandas, NumPy, SQL, PyTorch, Matplotlib, Git",
            "education": "B.Tech in Artificial Intelligence (CGPA: 9.1/10), Expected July 2026",
            "projects": [
                ("Research Intern - BITS AI Lab (2025 | 6 months)", "Fine-tuned BERT models for multilingual sentiment analysis. Published paper on transformer efficiency."),
                ("Automated Essay Scoring Model", "Created NLP pipeline using Python, Scikit-Learn, and spaCy for automated grammar and semantics evaluation.")
            ]
        },
        {
            "filename": "04_Rahul_Verma_Java_Backend_Fresher.pdf",
            "name": "Rahul Verma",
            "college": "Pune Institute of Computer Technology (PICT)",
            "degree": "Bachelor of Computer Applications (BCA)",
            "contact": "rahul.verma@gmail.com | +91 98444 55667 | Pune | github.com/rahulverma-dev",
            "summary": "Recent BCA graduate passionate about backend development, object-oriented programming, Java, Spring Boot, and MySQL relational database design.",
            "skills": "Java, Spring Boot, MySQL, SQL, REST API, Git, OOP, Data Structures, Linux",
            "education": "BCA - Bachelor of Computer Applications (First Class with Distinction - 82%), 2025",
            "projects": [
                ("Online Banking Microservices System", "Designed secure RESTful API backend using Java and Spring Boot with MySQL database management."),
                ("Library Management Portal", "Developed full-fledged desktop and web client for book inventory tracking using Java and SQL.")
            ]
        },
        {
            "filename": "05_Kevin_DSouza_Frontend_Student.pdf",
            "name": "Kevin D'Souza",
            "college": "St. Xavier's College",
            "degree": "B.Sc in Computer Science (3rd Year)",
            "contact": "kevin.dsouza@stxaviers.edu | +91 98555 66778 | Mumbai | github.com/kevind-ui",
            "summary": "Frontend-focused student developer with an eye for UI/UX, responsive web design, React, and modern CSS/Tailwind frameworks.",
            "skills": "React, JavaScript, HTML, CSS, Tailwind, Bootstrap, Git, Figma, Responsive Web",
            "education": "B.Sc in Computer Science (CGPA: 8.2/10), Expected 2026",
            "projects": [
                ("Crypto Portfolio Tracker Web App", "Engineered responsive client-side dashboard in React using CoinGecko public APIs."),
                ("Frontend Design Intern - IndieAgency (Summer 2025)", "Converted Figma designs into production-ready responsive web pages using HTML, CSS, and React.")
            ]
        },
        {
            "filename": "06_Pooja_Joshi_Cloud_DevOps_Student.pdf",
            "name": "Pooja Joshi",
            "college": "PES University, Bangalore",
            "degree": "B.Tech in Computer Science (4th Year)",
            "contact": "pooja.joshi@pes.edu | +91 98666 77889 | Bangalore | github.com/poojajoshi-cloud",
            "summary": "Undergraduate student passionate about cloud computing, AWS, containerization with Docker, and CI/CD automation pipelines.",
            "skills": "AWS, Docker, Linux, Python, Bash, Git, CI/CD, Kubernetes, Terraform",
            "education": "B.Tech in Computer Science (CGPA: 8.5/10), Expected 2026",
            "projects": [
                ("Automated Containerized CI/CD Pipeline", "Set up GitHub Actions workflow to build Docker images and deploy microservices to AWS EC2."),
                ("Cloud Architecture Capstone Project", "Designed scalable multi-tier web application architecture utilizing AWS S3, EC2, and RDS.")
            ]
        },
        {
            "filename": "07_Vikram_Malhotra_ECE_Fresher.pdf",
            "name": "Vikram Malhotra",
            "college": "Thapar University",
            "degree": "B.Tech in Electronics & Communication (ECE)",
            "contact": "vikram.malhotra@thapar.edu | +91 98777 88990 | Patiala",
            "summary": "ECE graduate with foundational training in embedded C, microcontrollers, basic Python scripting, and digital electronics.",
            "skills": "C, C++, Python, Embedded Systems, IoT, Arduino, MATLAB, Circuit Design",
            "education": "B.Tech in Electronics & Communication Engineering (CGPA: 7.6/10), 2025",
            "projects": [
                ("Smart Home Automation with IoT", "Engineered Arduino and Raspberry Pi sensor interface with wireless communication protocols."),
                ("MATLAB Signal Processing Filter", "Implemented digital filtering algorithms for audio noise cancellation.")
            ]
        },
        {
            "filename": "08_Riya_Sen_Marketing_Student.pdf",
            "name": "Riya Sen",
            "college": "Symbiosis Institute",
            "degree": "Bachelor of Business Administration (BBA - Marketing)",
            "contact": "riya.sen@siu.edu.in | +91 98888 99001 | Pune",
            "summary": "Final year BBA student specializing in digital marketing, campus brand ambassadorship, content writing, and social media campaigns.",
            "skills": "Digital Marketing, Social Media, Content Writing, SEO, Google Analytics, Brand Strategy, Market Research",
            "education": "BBA - Marketing (CGPA: 8.4/10), Expected 2026",
            "projects": [
                ("Campus Marketing Lead - YouthFest", "Orchestrated social media promotion generating 15,000+ student engagements across Instagram and LinkedIn."),
                ("Content Marketing Intern - MediaPulse (Summer 2025)", "Drafted weekly newsletter copy and analyzed Google Analytics audience demographics.")
            ]
        }
    ]

    for s in students:
        pdf_path = os.path.join(student_dir, s["filename"])
        create_pdf_student_resume(
            pdf_path,
            s["name"],
            s["college"],
            s["degree"],
            s["contact"],
            s["summary"],
            s["skills"],
            s["projects"],
            s["education"]
        )

    print(f"Generated {len(students)} realistic student/intern PDF resumes and {len(intern_jds)} campus JDs successfully.")


if __name__ == "__main__":
    generate_all_student_data()
