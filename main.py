"""
main.py — Command-line interface for the AI Resume Analyzer.

Usage:
    python main.py --resume resume.txt --jd job_description.txt --role data_analyst
    python main.py --resume resume.txt --jd job_description.txt --cover-letter
"""
from dotenv import load_dotenv
load_dotenv()
import argparse
import sys
from pathlib import Path
from src.analyzer import analyze_resume, generate_cover_letter
from src.rag import list_supported_roles


def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    p = Path(path)
    if not p.exists():
        print(f"Error: File not found — {path}")
        sys.exit(1)
    return p.read_text(encoding="utf-8").strip()


def print_analysis(result: dict) -> None:
    """Pretty-print the analysis result to the terminal."""
    print("\n" + "=" * 60)
    print("       AI RESUME ANALYZER — RESULTS")
    print("=" * 60)

    score = result.get("match_score")
    if score is not None:
        bar = "█" * (score // 5) + "░" * (20 - score // 5)
        print(f"\n  Match Score: {score}/100  [{bar}]")

    if result["strengths"]:
        print("\n✅  STRENGTHS")
        for item in result["strengths"]:
            print(f"   • {item}")

    if result["gaps"]:
        print("\n⚠️   GAPS / MISSING SKILLS")
        for item in result["gaps"]:
            print(f"   • {item}")

    if result["suggestions"]:
        print("\n💡  SUGGESTIONS")
        for item in result["suggestions"]:
            print(f"   • {item}")

    if result["keywords_missing"]:
        print("\n🔑  KEYWORDS TO ADD TO RESUME")
        for item in result["keywords_missing"]:
            print(f"   • {item}")

    print("\n" + "=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="AI Resume Analyzer — powered by OpenAI GPT-4 + RAG"
    )
    parser.add_argument("--resume", required=True, help="Path to resume text file")
    parser.add_argument("--jd", required=True, help="Path to job description text file")
    parser.add_argument(
        "--role",
        default="general",
        choices=list_supported_roles(),
        help="Role type for tailored analysis (default: general)",
    )
    parser.add_argument(
        "--cover-letter",
        action="store_true",
        help="Also generate a personalized cover letter",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional: save cover letter to a text file",
    )

    args = parser.parse_args()

    resume_text = read_file(args.resume)
    jd_text = read_file(args.jd)

    print(f"\n🔍  Analyzing resume for role: {args.role} ...")
    result = analyze_resume(resume_text, jd_text, role=args.role)
    print_analysis(result)

    if args.cover_letter:
        print("✍️   Generating cover letter ...")
        letter = generate_cover_letter(resume_text, jd_text, role=args.role)
        print("\n--- COVER LETTER ---\n")
        print(letter)
        print("\n--------------------\n")

        if args.output:
            Path(args.output).write_text(letter, encoding="utf-8")
            print(f"✅  Cover letter saved to: {args.output}")


if __name__ == "__main__":
    main()
