"""
utils.py: Helper utilities, skill taxonomy, canonical synonyms, and regex patterns for CV and JD parsing.
"""

import re
from typing import Dict, List, Set, Tuple

# Comprehensive domain skill taxonomy for technical & general roles
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "python", "java", "c++", "c", "c#", "javascript", "typescript", "golang", "go",
        "ruby", "rust", "php", "swift", "kotlin", "r", "scala", "shell", "bash", "sql"
    ],
    "AI, ML & Data Science": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "llm", "large language models", "genai", "generative ai",
        "transformers", "bert", "gpt", "rag", "langchain", "llamaindex", "faiss",
        "pytorch", "tensorflow", "keras", "scikit-learn", "sklearn", "pandas",
        "numpy", "scipy", "xgboost", "lightgbm", "opencv", "spacy", "nltk",
        "data analysis", "data visualization", "matplotlib", "seaborn", "tableau", "power bi"
    ],
    "Web & Backend Development": [
        "react", "react.js", "next.js", "vue", "vue.js", "angular", "node", "node.js", "nodejs",
        "express", "express.js", "django", "flask", "fastapi", "spring boot", "springboot",
        "asp.net", "html", "html5", "css", "css3", "tailwind", "bootstrap", "rest api", "apis",
        "restful", "graphql", "microservices"
    ],
    "Mobile & UI Design": [
        "react native", "flutter", "android studio", "android", "ios", "swift", "figma", "ui/ux", "responsive design"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker",
        "kubernetes", "k8s", "terraform", "ansible", "jenkins", "ci/cd", "github actions",
        "gitlab", "linux", "nginx", "helm", "prometheus", "grafana"
    ],
    "Databases & Big Data": [
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
        "cassandra", "dynamodb", "spark", "apache spark", "hadoop", "kafka",
        "snowflake", "bigquery"
    ],
    "Tools & Engineering Practices": [
        "git", "github", "jira", "agile", "scrum", "unit testing", "pytest",
        "system design", "oop", "object oriented programming", "data structures", "algorithms"
    ]
}

# Canonical synonym mapping to merge variations, abbreviations & suffixes (e.g. node.js vs node, react vs react.js)
CANONICAL_SYNONYMS: Dict[str, str] = {
    # Web & Full Stack
    "react": "React.js",
    "react.js": "React.js",
    "reactjs": "React.js",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express": "Express.js",
    "express.js": "Express.js",
    "expressjs": "Express.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "vuejs": "Vue.js",
    "angular": "Angular",
    "angular.js": "Angular",
    "angularjs": "Angular",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "tailwind": "Tailwind",
    "bootstrap": "Bootstrap",
    "rest api": "REST API",
    "rest apis": "REST API",
    "restful": "REST API",
    "restful api": "REST API",
    "apis": "REST API",
    "api": "REST API",
    "graphql": "GraphQL",
    "microservices": "Microservices",
    # Mobile & UI
    "react native": "React Native",
    "flutter": "Flutter",
    "android studio": "Android Studio",
    "android": "Android Studio",
    "figma": "Figma",
    "ui/ux": "UI/UX",
    "responsive design": "Responsive Design",
    # Databases
    "mongodb": "MongoDB",
    "mongo": "MongoDB",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "redis": "Redis",
    "sqlite": "SQLite",
    # AI & ML
    "nlp": "NLP",
    "natural language processing": "NLP",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "genai": "Generative AI",
    "generative ai": "Generative AI",
    "llm": "LLM",
    "large language models": "LLM",
    "large language model": "LLM",
    "transformers": "Transformers",
    "bert": "BERT",
    "gpt": "GPT",
    "rag": "RAG",
    "langchain": "LangChain",
    "llamaindex": "LlamaIndex",
    "faiss": "FAISS",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    # Cloud & DevOps
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "GCP",
    "google cloud": "GCP",
    "azure": "Azure",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "jenkins": "Jenkins",
    "ci/cd": "CI/CD",
    "linux": "Linux",
    "git": "Git",
    "github": "GitHub",
    "data structures": "Data Structures",
    "algorithms": "Algorithms"
}

# Flattened set of all known skills for fast lookup
ALL_CANONICAL_SKILLS: Set[str] = {
    skill.lower()
    for skills in SKILL_TAXONOMY.values()
    for skill in skills
}

# Common degree keywords
DEGREE_KEYWORDS = [
    r"\bb\.?\s*tech\b", r"\bb\.?\s*e\b", r"\bm\.?\s*tech\b", r"\bm\.?\s*s\b",
    r"\bmca\b", r"\bbca\b", r"\bbachelor(?:'s)?\b", r"\bmaster(?:'s)?\b",
    r"\bph\.?d\b", r"\bb\.?\s*sc\b", r"\bm\.?\s*sc\b", r"\bdiploma\b"
]


def clean_text(text: str) -> str:
    """Normalize whitespace and remove excessive control characters."""
    if not text:
        return ""
    text = re.sub(r"[\r\n]+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_email(text: str) -> str:
    """Extract email address from document text."""
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group(0).lower() if match else "Not specified"


def extract_phone(text: str) -> str:
    """Extract phone number (supports Indian and international formats)."""
    pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b"
    match = re.search(pattern, text)
    return match.group(0) if match else "Not specified"


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills present in text using canonical synonym mapping and punctuation boundaries.
    """
    found_skills: Set[str] = set()
    text_lower = f" {text.lower()} "

    # Check canonical synonyms (ordered by length descending to match compound terms first)
    sorted_synonyms = sorted(CANONICAL_SYNONYMS.keys(), key=len, reverse=True)
    for term in sorted_synonyms:
        escaped_term = re.escape(term)
        # Match with boundary punctuation (whitespace, commas, periods, colons, brackets, dashes)
        pattern = rf"(?:^|[\s,;:\(\)\[\]/.-]){escaped_term}(?:$|[\s,;:\(\)\[\]/.-])"
        if re.search(pattern, text_lower):
            found_skills.add(CANONICAL_SYNONYMS[term])

    # Check any remaining unmapped skills
    for skill in ALL_CANONICAL_SKILLS:
        if skill in CANONICAL_SYNONYMS:
            continue
        escaped_skill = re.escape(skill)
        pattern = rf"(?:^|[\s,;:\(\)\[\]/.-]){escaped_skill}(?:$|[\s,;:\(\)\[\]/.-])"
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())

    return sorted(list(found_skills))


def extract_years_of_experience(text: str) -> float:
    """
    Heuristic detection of years of experience from resume/JD text.
    Handles explicit years, fresher ranges, and employment date ranges (e.g. 2014-2019, 2018-Present).
    """
    text_lower = text.lower()

    # If it is a fresher / intern range like 0-2 or 0-1, return 0.0
    if re.search(r"\b0\s*[-–to]\s*\d+\s*(?:years?|yrs?)", text_lower) or "intern" in text_lower or "fresher" in text_lower:
        if "intern" in text_lower and not re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", text_lower):
            return 0.5

    # 1. Check explicit 'X years of experience' patterns
    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)",
        r"(?:experience|exp):\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)?",
        r"over\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s+in\s+[a-zA-Z]+"
    ]

    max_years = 0.0
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            try:
                val = float(match)
                if 0.5 <= val <= 35:
                    if val > max_years:
                        max_years = val
            except ValueError:
                continue

    # 2. Parse employment date ranges (e.g. 2012 to 2018, 2019 - Present)
    date_ranges = re.findall(r"\b(19[89]\d|20[012]\d)\s*(?:[-–to]+|\s+to\s+)\s*(19[89]\d|20[012]\d|present|current)\b", text_lower)
    if date_ranges:
        date_years = 0.0
        for s, e in date_ranges:
            try:
                start_yr = int(s)
                end_yr = 2026 if e in ['present', 'current'] else int(e)
                diff = max(0, min(15, end_yr - start_yr))
                date_years += diff
            except ValueError:
                continue
        if date_years > max_years:
            max_years = min(30.0, date_years)

    return max_years


def extract_education(text: str) -> List[str]:
    """Detect degrees and qualifications in the text."""
    found_degrees: Set[str] = set()
    text_lower = text.lower()

    for pattern in DEGREE_KEYWORDS:
        if re.search(pattern, text_lower):
            cleaned_label = pattern.replace(r"\b", "").replace(r"\.?", "").replace(r"\s*", " ").replace(r"(?:'s)?", "").strip()
            found_degrees.add(cleaned_label.upper())

    return sorted(list(found_degrees))
