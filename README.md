# HireIQ — AI Talent Screener

An enterprise-level AI-powered resume screening system that ranks and shortlists candidates using RAG pipeline, semantic search, and knowledge graphs.

## Features
- Multi-resume upload and parallel processing
- RAG pipeline with FAISS vector search for semantic matching
- Knowledge Graph extraction using Neo4j
- AI scoring and candidate ranking via Groq LLM
- Export results to PDF, Excel, and Word
- Shortlist email to HR
- Dashboard analytics with charts
- HR login authentication

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
*(Add screenshots here)*
