# 🤖 AI Resume Analyzer

A Python-based application that analyzes resumes against job descriptions using Google Gemini AI, providing match scores, skill gap analysis, and personalized cover letter generation.

## ✨ Features
- **Resume Analysis** — Match score, strengths, gaps, and missing keywords
- **Cover Letter Generation** — Personalized, role-specific cover letters
- **RAG Pipeline** — Retrieval-Augmented Generation for role-specific context
- **Modular Prompt Engineering** — Easy role customization with minimal code changes

## 🛠️ Tech Stack
Python · Google Gemini API · RAG · Prompt Engineering

## 🚀 Setup

```bash
git clone https://github.com/KaranKapoor404/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

Get your free API key at [aistudio.google.com](https://aistudio.google.com)

## 💻 Usage

```bash
# Analyze resume
python main.py --resume your_resume.txt --jd job_description.txt --role data_analyst

# With cover letter
python main.py --resume your_resume.txt --jd job_description.txt --role data_analyst --cover-letter
```

## 🎯 Supported Roles
`data_analyst` · `software_engineer` · `product_manager` · `general`

## 📁 Project Structure
```
ai-resume-analyzer/
├── main.py
├── src/
│   ├── analyzer.py       # Gemini API integration
│   ├── rag.py            # RAG context retrieval
│   └── prompt_builder.py # Modular prompt templates
└── examples/
    ├── sample_resume.txt
    └── sample_jd.txt
```
