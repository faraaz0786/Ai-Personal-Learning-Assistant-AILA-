# AILA: Scholarly AI Workspace 🎓🤖

**Scholarly AI Workspace (AILA)** is a premium, production-grade learning assistant designed for researchers, students, and lifelong learners. It transforms static study material into interactive, intelligence-driven learning paths.

![AILA Dashboard](https://raw.githubusercontent.com/faraaz0786/Ai-Personal-Learning-Assistant-AILA-/main/docs/screenshots/dashboard.png)

## ✨ Key Features
- **Intellectual Progress Tracking**: Real-time weighted scoring system (Coverage, Accuracy, Quiz performance).
- **AI Mentor Insights**: Context-aware study tips based on your recent learning behavior.
- **Dynamic Learning Library**: A persistent, searchable archive of all learned topics and summaries.
- **AI Tutor Engine**: Natural language explanations and structured knowledge synthesis.
- **SaaS-Grade UI**: A warm, scholarly aesthetic featuring Ivory/Burnt Orange accents and editorial typography.

## 🛠 Tech Stack
- **Frontend**: React, Vite, Zustand, React-Query, Vanilla CSS.
- **Backend**: FastAPI (Python), SQLAlchemy, Pydantic.
- **LLM**: Groq (Llama-3 architecture).
- **Database**: Supabase (PostgreSQL).
- **Deployment**: Vercel (Monorepo).

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/faraaz0786/Ai-Personal-Learning-Assistant-AILA-.git
cd AI-Personal-Learning-Assistant
```

### 2. Environment Setup
Create a `.env` file from the template:
```bash
cp .env.example .env
```
Fill in your `DATABASE_URL` and `GROQ_API_KEY`.

### 3. Backend Setup
```bash
# Recommended: Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8003
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📂 Documentation
- [System Architecture](docs/Architecture.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/Deployment.md)

---
Developed by **Faraaz** — [GitHub](https://github.com/faraaz0786)
