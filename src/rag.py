"""
rag.py — Lightweight Retrieval-Augmented Generation layer.

Instead of a full vector database, this module uses a curated knowledge base
of role-specific hiring criteria stored as structured dictionaries.
This simulates RAG by injecting relevant domain context into prompts,
improving output relevance without requiring an external vector store.

To scale this up: replace `KNOWLEDGE_BASE` with embeddings + FAISS/Chroma lookups.
"""

from typing import Optional

# ---------------------------------------------------------------------------
# Knowledge base — role-specific hiring context
# Each entry contains: required_skills, nice_to_have, common_jd_keywords,
#                       red_flags, and evaluation_focus.
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "data_analyst": {
        "required_skills": ["SQL", "Python", "Excel", "data visualization", "statistics"],
        "nice_to_have": ["Power BI", "Tableau", "DAX", "BigQuery", "dbt", "Looker"],
        "common_jd_keywords": [
            "data-driven", "KPI", "dashboard", "ETL", "A/B testing",
            "stakeholder reporting", "ad hoc analysis",
        ],
        "red_flags": ["no quantified impact", "vague project descriptions", "missing SQL"],
        "evaluation_focus": (
            "Focus on SQL proficiency, ability to turn raw data into business insights, "
            "and experience with BI tools. Quantified achievements are critical."
        ),
    },
    "python_developer": {
        "required_skills": ["Python", "REST APIs", "Git", "OOP", "unit testing"],
        "nice_to_have": ["FastAPI", "Docker", "PostgreSQL", "Redis", "CI/CD", "AWS"],
        "common_jd_keywords": [
            "backend", "microservices", "API design", "async", "scalability",
            "code review", "Agile",
        ],
        "red_flags": ["no GitHub link", "only Jupyter notebooks", "no production experience"],
        "evaluation_focus": (
            "Assess code quality signals: GitHub activity, deployed projects, "
            "testing habits, and experience with production-grade Python."
        ),
    },
    "ai_ml_engineer": {
        "required_skills": ["Python", "machine learning", "scikit-learn", "pandas", "NumPy"],
        "nice_to_have": [
            "PyTorch", "TensorFlow", "LangChain", "OpenAI API",
            "MLflow", "Hugging Face", "vector databases",
        ],
        "common_jd_keywords": [
            "model training", "fine-tuning", "LLM", "RAG", "prompt engineering",
            "inference", "feature engineering", "MLOps",
        ],
        "red_flags": ["only theoretical ML", "no deployed models", "missing evaluation metrics"],
        "evaluation_focus": (
            "Look for end-to-end ML project experience: data → model → deployment. "
            "LLM/GenAI exposure is a strong differentiator in 2024."
        ),
    },
    "general": {
        "required_skills": ["communication", "problem solving", "relevant domain tools"],
        "nice_to_have": ["leadership", "cross-functional collaboration", "data literacy"],
        "common_jd_keywords": ["results-driven", "collaborative", "ownership", "impact"],
        "red_flags": ["no measurable achievements", "unexplained employment gaps"],
        "evaluation_focus": (
            "Assess overall fit: relevant experience, measurable impact, "
            "and alignment with stated responsibilities."
        ),
    },
}


def retrieve_relevant_context(role: str) -> str:
    """
    Retrieve a formatted context string for the given role.

    Args:
        role: One of "data_analyst", "python_developer", "ai_ml_engineer", "general"

    Returns:
        A formatted string injected into the prompt as domain context.
    """
    entry = KNOWLEDGE_BASE.get(role, KNOWLEDGE_BASE["general"])

    context = f"""
--- ROLE-SPECIFIC HIRING CONTEXT (use this to calibrate your evaluation) ---
Required Skills:      {", ".join(entry["required_skills"])}
Nice-to-Have Skills:  {", ".join(entry["nice_to_have"])}
Common JD Keywords:   {", ".join(entry["common_jd_keywords"])}
Red Flags to Check:   {", ".join(entry["red_flags"])}
Evaluation Guidance:  {entry["evaluation_focus"]}
--- END CONTEXT ---
""".strip()

    return context


def list_supported_roles() -> list[str]:
    """Return all roles with knowledge base entries."""
    return list(KNOWLEDGE_BASE.keys())
