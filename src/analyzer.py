"""
analyzer.py — Core resume analysis engine using google-genai SDK.
"""

import os
from google import genai
from src.prompt_builder import build_analysis_prompt, build_cover_letter_prompt
from src.rag import retrieve_relevant_context

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume(resume_text: str, job_description: str, role: str = "general") -> dict:
    context = retrieve_relevant_context(role)
    prompt = build_analysis_prompt(
        resume_text=resume_text,
        job_description=job_description,
        role=role,
        context=context,
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return _parse_analysis(response.text)


def generate_cover_letter(resume_text: str, job_description: str, role: str = "general") -> str:
    context = retrieve_relevant_context(role)
    prompt = build_cover_letter_prompt(
        resume_text=resume_text,
        job_description=job_description,
        role=role,
        context=context,
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()


def _parse_analysis(raw_text: str) -> dict:
    result = {
        "match_score": None,
        "strengths": [],
        "gaps": [],
        "suggestions": [],
        "keywords_missing": [],
        "raw": raw_text,
    }

    current_section = None
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        lower = line.lower()
        if "match score" in lower:
            parts = line.split(":")
            if len(parts) > 1:
                score_str = parts[1].strip().split("/")[0].strip()
                try:
                    result["match_score"] = int(score_str)
                except ValueError:
                    pass
            current_section = None
        elif "strength" in lower:
            current_section = "strengths"
        elif "gap" in lower or "missing skill" in lower:
            current_section = "gaps"
        elif "suggestion" in lower or "recommendation" in lower:
            current_section = "suggestions"
        elif "keyword" in lower:
            current_section = "keywords_missing"
        elif current_section and line.startswith(("-", "•", "*")):
            result[current_section].append(line.lstrip("-•* "))

    return result