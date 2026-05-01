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
<img width="1920" height="1019" alt="Screenshot (553)" src="https://github.com/user-attachments/assets/58c6d9b9-5bb7-43f6-ad4a-fa0cef75c284" />
<img width="1920" height="1005" alt="Screenshot (562)" src="https://github.com/user-attachments/assets/8b924d90-084a-46ba-9faf-f990d538145b" />
<img width="1920" height="1015" alt="Screenshot (569)" src="https://github.com/user-attachments/assets/1b2d63b0-32d1-4b02-b64b-c17d788f834b" />
<img width="1920" height="1015" alt="Screenshot (570)" src="https://github.com/user-attachments/assets/d15c39fc-7561-4781-8878-3126c8ef9ef7" />
<img width="1920" height="1022" alt="Screenshot (574)" src="https://github.com/user-attachments/assets/66a0db2e-2a2e-46bd-992f-276bd535147a" />
<img width="1920" height="1025" alt="Screenshot (575)" src="https://github.com/user-attachments/assets/df87a0f5-8c7c-4a8f-8dd6-6b763b99139b" />

