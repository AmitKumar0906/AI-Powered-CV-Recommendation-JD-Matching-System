"""
parser.py: Extract and parse resumes (PDF/DOCX/TXT) and Job Descriptions into structured dictionaries.
"""

import io
import os
import re
from typing import Any, Dict, Optional, Union
import pypdf
from docx import Document

from src.utils import (
    clean_text,
    extract_education,
    extract_email,
    extract_phone,
    extract_skills_from_text,
    extract_years_of_experience,
)


class DocumentParser:
    """Handles text extraction and structured parsing of resumes and JDs."""

    @staticmethod
    def extract_text_from_pdf(file_source: Union[str, io.BytesIO]) -> str:
        """Extract plain text from a PDF file path or byte buffer."""
        text = ""
        try:
            reader = pypdf.PdfReader(file_source)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        except Exception as e:
            text = f"Error reading PDF: {e}"
        return clean_text(text)

    @staticmethod
    def extract_text_from_docx(file_source: Union[str, io.BytesIO]) -> str:
        """Extract plain text from a DOCX file path or byte buffer."""
        text = ""
        try:
            doc = Document(file_source)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            text = f"Error reading DOCX: {e}"
        return clean_text(text)

    @classmethod
    def extract_text(cls, file_source: Union[str, io.BytesIO], filename: Optional[str] = None) -> str:
        """Universal text extractor based on file extension."""
        name = ""
        if isinstance(file_source, str):
            name = file_source.lower()
        elif filename:
            name = filename.lower()

        if name.endswith(".pdf"):
            return cls.extract_text_from_pdf(file_source)
        elif name.endswith(".docx") or name.endswith(".doc"):
            return cls.extract_text_from_docx(file_source)
        else:
            if isinstance(file_source, str) and os.path.isfile(file_source):
                with open(file_source, "r", encoding="utf-8", errors="ignore") as f:
                    return clean_text(f.read())
            elif isinstance(file_source, io.BytesIO):
                return clean_text(file_source.getvalue().decode("utf-8", errors="ignore"))
            return clean_text(str(file_source))

    @staticmethod
    def extract_candidate_name(text: str, fallback_filename: Optional[str] = None) -> str:
        """
        Extract candidate name from document header or filename fallback.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:5]:
            # Look for lines that look like person names (2 to 4 words, letters only)
            if re.match(r"^[A-Z][a-zA-Z\.\'-]+(?:\s+[A-Z][a-zA-Z\.\'-]+){1,3}$", line):
                # Ensure it's not a resume header like "CURRICULUM VITAE" or "RESUME"
                if line.upper() not in ["CURRICULUM VITAE", "RESUME", "JOB DESCRIPTION", "PROFILE SUMMARY"]:
                    return line

        if fallback_filename:
            base = os.path.splitext(os.path.basename(fallback_filename))[0]
            clean_name = re.sub(r"[-_]+", " ", base).replace("Resume", "").replace("CV", "").strip()
            if clean_name.isdigit():
                first_line = lines[0] if lines else "Applicant"
                if len(first_line) <= 45 and not any(kw in first_line.upper() for kw in ["CURRICULUM", "RESUME", "PROFILE"]):
                    return f"Candidate #{clean_name} ({first_line.title()})"
                return f"Candidate #{clean_name}"
            elif clean_name:
                return clean_name.title()

        return "Candidate"

    @classmethod
    def parse_resume(cls, file_source: Union[str, io.BytesIO], filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse raw resume into a structured candidate dictionary.
        """
        raw_text = cls.extract_text(file_source, filename)
        name = cls.extract_candidate_name(raw_text, filename)
        email = extract_email(raw_text)
        phone = extract_phone(raw_text)
        skills = extract_skills_from_text(raw_text)
        experience_yrs = extract_years_of_experience(raw_text)
        education = extract_education(raw_text)

        display_filename = filename if filename else (os.path.basename(file_source) if isinstance(file_source, str) else "uploaded_resume")

        return {
            "filename": display_filename,
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience_years": experience_yrs,
            "education": education,
            "raw_text": raw_text,
            "text_length": len(raw_text)
        }

    @classmethod
    def parse_job_description(cls, text_or_source: Union[str, io.BytesIO], filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse Job Description text into structured requirements.
        """
        if isinstance(text_or_source, io.BytesIO) or (isinstance(text_or_source, str) and (text_or_source.endswith(".pdf") or text_or_source.endswith(".docx"))):
            raw_text = cls.extract_text(text_or_source, filename)
        else:
            raw_text = clean_text(str(text_or_source))

        skills = extract_skills_from_text(raw_text)
        min_experience = extract_years_of_experience(raw_text)

        # Intern / Fresher role detection (requires 0 years)
        if any(term in raw_text.lower() for term in ["intern", "internship", "fresher", "0-2", "0–2", "0 to 2"]):
            min_experience = 0.0

        # Detect and clean role title from top lines
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        raw_title = lines[0] if lines else "Target Position"
        # Strip markdown header hashes and 'Job Description:' prefixes
        clean_title = re.sub(r"^[#\s*]+(?:job\s+description:?\s*)?", "", raw_title, flags=re.IGNORECASE).strip()
        if len(clean_title) > 60:
            clean_title = clean_title[:60] + "..."

        return {
            "title": clean_title,
            "raw_text": raw_text,
            "required_skills": skills,
            "min_experience_years": min_experience
        }
