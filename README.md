# HireIQ AI-Powered Talent Screener

> Enterprise-grade resume screening system using RAG pipeline, Knowledge Graph, and LLM scoring.

**Live Demo:** [hireiq-ai-talent-screener-production.up.railway.app](https://hireiq-ai-talent-screener-production.up.railway.app)

---

## Problem It Solves

Traditional resume screening is manual, slow, and keyword-dependent. HireIQ uses semantic search and AI scoring to match candidates against job descriptions — going beyond keywords to understand context and relationships.

---

## Architecture

```
PDF Resume(s)
↓
Text Extraction (pypdf)
↓
Chunking + Embedding (HuggingFace: all-MiniLM-L6-v2)
↓
FAISS Vector Store
↓
RAG Pipeline (LangChain + Groq LLM: Llama 3.3 70B)
↓
Match Score (0-100) + Detailed Analysis
↓
Knowledge Graph Extraction → Neo4j
↓
Ranked Results + Dashboard Analytics
```

---

## Features

- Multi-resume upload with parallel processing
- Semantic similarity scoring using RAG pipeline
- Knowledge Graph for skill and relationship mapping (Neo4j)
- Detailed AI analysis per candidate (strengths, weaknesses, recommendations)
- Candidate ranking with Shortlisted / Review / Rejected status
- Export results to PDF, Excel, Word
- HR shortlist email integration (Gmail SMTP)
- Dashboard analytics with charts (Chart.js)
- HR authentication system (session-based login)
- Deployed on Railway

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI / LLM | Groq (Llama 3.3 70B), LangChain |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector DB | FAISS |
| Graph DB | Neo4j Aura |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Export | fpdf2, openpyxl, python-docx |
| Email | smtplib (Gmail SMTP) |
| Deployment | Railway |

---

## How It Works

1. HR logs in with credentials
2. Uploads one or more PDF resumes
3. Enters job description
4. System runs RAG pipeline — extracts text, creates vectors, scores each candidate
5. Knowledge Graph maps skills and relationships per candidate
6. Results show ranked candidates with scores, analysis, and status
7. HR exports shortlist or sends email to hiring team

---

## Run Locally

```bash
git clone https://github.com/Iamfouzia/HireIQ-AI-Talent-Screener.git
cd HireIQ-AI-Talent-Screener
pip install -r requirements.txt
```

Create `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key
NEO4J_URI=your_neo4j_uri
NEO4J_PASSWORD=your_neo4j_password
EMAIL_ADDRESS=your_gmail
EMAIL_PASSWORD=your_gmail_app_password
HR_USERNAME=admin
HR_PASSWORD=your_password
SECRET_KEY=your_secret_key
```

Run the app:

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM |
| `NEO4J_URI` | Neo4j Aura connection URI |
| `NEO4J_PASSWORD` | Neo4j database password |
| `EMAIL_ADDRESS` | Gmail address for sending emails |
| `EMAIL_PASSWORD` | Gmail App Password |
| `HR_USERNAME` | Login username |
| `HR_PASSWORD` | Login password |
| `SECRET_KEY` | Flask session secret key |

---

## Results

| Metric | Value |
|---|---|
| Scoring method | RAG + semantic similarity |
| LLM model | Llama 3.3 70B via Groq |
| Embedding model | all-MiniLM-L6-v2 |
| Graph nodes extracted | Up to 80+ per session |
| Export formats | PDF, Excel, Word |
| Auth | Session-based HR login |

---

## Project Structure

```
HireIQ-AI-Talent-Screener/
├── app.py               # Flask server, routes, auth
├── rag_pipeline.py      # RAG pipeline, FAISS, scoring
├── graph_builder.py     # Knowledge Graph, Neo4j
├── templates/
│   ├── index.html       # Main dashboard
│   └── login.html       # HR login page
├── static/
│   └── style.css        # Styling
├── uploads/             # Uploaded resumes (gitignored)
├── .env                 # API keys (gitignored)
└── requirements.txt     # Dependencies
```

























# HireIQ AI-Powered Talent Screener

> Enterprise-grade resume screening system using RAG pipeline, Knowledge Graph, and LLM scoring.

**Live Demo:** [hireiq-ai-talent-screener-production.up.railway.app](https://hireiq-ai-talent-screener-production.up.railway.app)

## Problem It Solves

Traditional resume screening is manual, slow, and keyword-dependent. HireIQ uses semantic search and AI scoring to match candidates against job descriptions — going beyond keywords to understand context and relationships.

## Architecture
PDF Resume(s)
↓
Text Extraction (pypdf)
↓
Chunking + Embedding (HuggingFace: all-MiniLM-L6-v2)
↓
FAISS Vector Store
↓
RAG Pipeline (LangChain + Groq LLM: Llama 3.3 70B)
↓
Match Score (0-100) + Detailed Analysis
↓
Knowledge Graph Extraction → Neo4j
↓
Ranked Results + Dashboard Analytics


## Features
- Multi-resume upload with parallel processing
- Semantic similarity scoring using RAG pipeline
- Knowledge Graph for skill and relationship mapping (Neo4j)
- Detailed AI analysis per candidate (strengths, weaknesses, recommendations)
- Candidate ranking with Shortlisted / Review / Rejected status
- Export results to PDF, Excel, Word
- HR shortlist email integration (Gmail SMTP)
- Dashboard analytics with charts (Chart.js)
- HR authentication system (session-based login)
- Deployed on Railway


## Tech Stack

| Layer | Technology |
| Backend | Python, Flask |
| AI / LLM | Groq (Llama 3.3 70B), LangChain |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector DB | FAISS |
| Graph DB | Neo4j Aura |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Export | fpdf2, openpyxl, python-docx |
| Email | smtplib (Gmail SMTP) |
| Deployment | Railway |

---

## How It Works

1. HR logs in with credentials
2. Uploads one or more PDF resumes
3. Enters job description
4. System runs RAG pipeline — extracts text, creates vectors, scores each candidate
5. Knowledge Graph maps skills and relationships per candidate
6. Results show ranked candidates with scores, analysis, and status
7. HR exports shortlist or sends email to hiring team

---

## Run Locally

```bash
git clone https://github.com/Iamfouzia/HireIQ-AI-Talent-Screener.git
cd HireIQ-AI-Talent-Screener
pip install -r requirements.txt

Create `.env` file:
GROQ_API_KEY=your_groq_api_key
NEO4J_URI=your_neo4j_uri
NEO4J_PASSWORD=your_neo4j_password
EMAIL_ADDRESS=your_gmail
EMAIL_PASSWORD=your_gmail_app_password
HR_USERNAME=admin
HR_PASSWORD=your_password
SECRET_KEY=your_secret_key

Run:

```bash
python app.py
```

Open: `http://127.0.0.1:5000`

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM |
| `NEO4J_URI` | Neo4j Aura connection URI |
| `NEO4J_PASSWORD` | Neo4j database password |
| `EMAIL_ADDRESS` | Gmail address for sending emails |
| `EMAIL_PASSWORD` | Gmail App Password |
| `HR_USERNAME` | Login username |
| `HR_PASSWORD` | Login password |
| `SECRET_KEY` | Flask session secret key |

---

## Results

| Metric | Value |
|---|---|
| Scoring method | RAG + semantic similarity |
| LLM model | Llama 3.3 70B via Groq |
| Embedding model | all-MiniLM-L6-v2 |
| Graph nodes extracted | Up to 80+ per session |
| Export formats | PDF, Excel, Word |
| Auth | Session-based HR login |


## Project Structure
HireIQ-AI-Talent-Screener/
├── app.py               # Flask server, routes, auth
├── rag_pipeline.py      # RAG pipeline, FAISS, scoring
├── graph_builder.py     # Knowledge Graph, Neo4j
├── templates/
│   ├── index.html       # Main dashboard
│   └── login.html       # HR login page
├── static/
│   └── style.css        # Styling
├── uploads/             # Uploaded resumes (gitignored)
├── .env                 # API keys (gitignored)
└── requirements.txt     # Dependencies























## Tech Stack
- **Backend:** Python, Flask
- **AI/ML:** LangChain, FAISS, Groq LLM, HuggingFace Embeddings
- **Graph DB:** Neo4j
- **Frontend:** HTML, CSS, JavaScript, Chart.js

## Setup

1. Clone the repo
2. Install dependencies
```bash
   pip install -r requirements.txt
```
3. Add `.env` file
GROQ_API_KEY=your_key
NEO4J_URI=your_uri
NEO4J_PASSWORD=your_password
EMAIL_ADDRESS=your_email
EMAIL_PASSWORD=your_app_password
HR_USERNAME=admin
HR_PASSWORD=your_password
SECRET_KEY=your_secret

4. Run the app
```bash
   python app.py
```
5. Open `http://127.0.0.1:5000`

## Screenshots
<img width="1920" height="1019" alt="Screenshot (553)" src="https://github.com/user-attachments/assets/58c6d9b9-5bb7-43f6-ad4a-fa0cef75c284" />
<img width="1920" height="1005" alt="Screenshot (562)" src="https://github.com/user-attachments/assets/8b924d90-084a-46ba-9faf-f990d538145b" />
<img width="1920" height="1015" alt="Screenshot (569)" src="https://github.com/user-attachments/assets/1b2d63b0-32d1-4b02-b64b-c17d788f834b" />
<img width="1920" height="1015" alt="Screenshot (570)" src="https://github.com/user-attachments/assets/d15c39fc-7561-4781-8878-3126c8ef9ef7" />
<img width="1920" height="1022" alt="Screenshot (574)" src="https://github.com/user-attachments/assets/66a0db2e-2a2e-46bd-992f-276bd535147a" />
<img width="1920" height="1025" alt="Screenshot (575)" src="https://github.com/user-attachments/assets/df87a0f5-8c7c-4a8f-8dd6-6b763b99139b" />

