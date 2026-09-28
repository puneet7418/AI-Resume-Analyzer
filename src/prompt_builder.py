"""
prompt_builder.py — Modular prompt engineering framework.

Each function returns a fully constructed prompt string.
Role-specific customization is handled here — adding a new role
only requires adding a template entry; no other code changes needed.
"""

from typing import Optional

# ---------------------------------------------------------------------------
# Role-specific prompt adjustments
# These tweak tone/focus without changing the core template structure.
# ---------------------------------------------------------------------------
ROLE_INSTRUCTIONS = {
    "data_analyst": (
        "Pay special attention to SQL depth, BI tool experience, "
        "and whether impact is quantified (%, ₹, time saved, rows processed)."
    ),
    "python_developer": (
        "Check for production-grade Python: deployed APIs, test coverage, "
        "Docker/CI usage, and public GitHub contributions."
    ),
    "ai_ml_engineer": (
        "Prioritize end-to-end ML pipelines, LLM/GenAI experience, "
        "deployed models, and familiarity with modern AI frameworks."
    ),
    "general": (
        "Evaluate overall fit, transferable skills, and alignment "
        "with the responsibilities listed in the job description."
    ),
}


def build_analysis_prompt(
    resume_text: str,
    job_description: str,
    role: str,
    context: str,
    Optional_notes: Optional[str] = None,
) -> str:
    """
    Build the resume analysis prompt.

    The prompt follows a structured template that instructs GPT to output
    clearly labeled sections — making it easy to parse programmatically.

    Args:
        resume_text:      Full resume content.
        job_description:  Full job posting content.
        role:             Role key for customization.
        context:          RAG-retrieved domain context string.
        Optional_notes:   Any extra instructions (e.g., "focus on Python skills").

    Returns:
        Complete prompt string ready for the OpenAI API.
    """
    role_instruction = ROLE_INSTRUCTIONS.get(role, ROLE_INSTRUCTIONS["general"])
    extra = f"\nAdditional Instructions: {Optional_notes}" if Optional_notes else ""

    prompt = f"""
You are evaluating a job application. Use the context below to calibrate your analysis.

{context}

Role-Specific Focus:
{role_instruction}
{extra}

======== RESUME ========
{resume_text}
========================

======== JOB DESCRIPTION ========
{job_description}
=================================

Provide your evaluation in EXACTLY this format (keep the labels):

Match Score: [number]/100

Strengths:
- [strength 1]
- [strength 2]
- [strength 3]

Gaps / Missing Skills:
- [gap 1]
- [gap 2]

Suggestions:
- [actionable suggestion 1]
- [actionable suggestion 2]

Keywords Missing from Resume:
- [keyword 1]
- [keyword 2]

Be direct. Do not pad with generic advice. Focus on what is specific to THIS resume and THIS role.
""".strip()

    return prompt


def build_cover_letter_prompt(
    resume_text: str,
    job_description: str,
    role: str,
    context: str,
) -> str:
    """
    Build the cover letter generation prompt.

    Args:
        resume_text:     Full resume content.
        job_description: Full job posting content.
        role:            Role key for tone/focus adjustment.
        context:         RAG-retrieved domain context string.

    Returns:
        Complete prompt string for cover letter generation.
    """
    role_instruction = ROLE_INSTRUCTIONS.get(role, ROLE_INSTRUCTIONS["general"])

    prompt = f"""
Write a personalized, professional cover letter for this job application.

{context}

Role Focus: {role_instruction}

======== RESUME ========
{resume_text}
========================

======== JOB DESCRIPTION ========
{job_description}
=================================

Guidelines:
- Open with a strong hook — not "I am writing to express my interest"
- Highlight 2–3 specific achievements from the resume that directly match the JD
- Use keywords from the job description naturally
- Keep it to 3 short paragraphs (under 250 words)
- End with a clear call to action
- Tone: confident, human, direct — not corporate or robotic
""".strip()

    return prompt


def build_keyword_extraction_prompt(job_description: str) -> str:
    """
    Build a prompt to extract ATS keywords from a job description.
    Useful as a standalone utility before resume tailoring.
    """
    return f"""
Extract the most important ATS (Applicant Tracking System) keywords from this job description.

======== JOB DESCRIPTION ========
{job_description}
=================================

Return:
1. Must-have technical skills (tools, languages, frameworks)
2. Soft skills or competencies explicitly mentioned
3. Industry/domain keywords
4. Action verbs used in responsibilities

Format as bullet points under each category. Be specific — not generic.
""".strip()
