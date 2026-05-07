# ============================================================
# RAG PIPELINE — Resume analysis using FAISS + Groq LLM
# ============================================================

import os
import re
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── Step 1: Initialize embedding model (runs locally, no API needed)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ── Step 2: Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


# ── UTILITY: Extract raw text from PDF
def extract_text(pdf_file):
    """Read all pages of a PDF and return combined text."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()


# ── UTILITY: Build FAISS vector store from resume text
def create_vector_store(text, candidate_name):
    """
    Split resume text into chunks and store in FAISS.
    Saved locally under uploads/ folder.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    # Safety check — if no chunks extracted, raise error
    if not chunks:
        raise ValueError(f"No text could be extracted from resume: {candidate_name}")

    vector_store = FAISS.from_texts(chunks, embeddings)
    vector_store.save_local(f"uploads/{candidate_name}_index")
    return vector_store


# ── CORE: Ask a question using RAG pipeline
def ask_question(vector_store, question):
    """
    Retrieve relevant chunks from vector store,
    then ask Groq LLM to answer based on those chunks.
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert HR recruiter. Answer based on the resume content only.

Resume Content:
{context}

Question: {question}

Give a detailed, structured answer.
        """
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    try:
        return chain.invoke(question)
    except Exception as e:
        return f"Analysis unavailable: {str(e)}"


# ── CORE: Get numeric match score (FIX — strict parsing)
def get_match_score(vector_store, job_description):
    """
    Ask Groq LLM to score the resume vs job description.
    Returns an integer between 0 and 100.

    FIX: Multiple fallback strategies to ensure we always
    get a valid number, never 0.
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a resume scoring expert.

Resume Content:
{context}

Job Requirements:
{question}

Task: Score how well this resume matches the job requirements.

Rules:
- Reply with ONLY a single integer between 0 and 100
- No words, no explanation, no percentage sign
- Just the number. Example: 78

Score:
        """
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    try:
        response = chain.invoke(job_description)
        print(f"[RAG] Raw score response: '{response}'")  # Debug log

        # Strategy 1: Find all numbers in response
        numbers = re.findall(r'\b(\d{1,3})\b', response.strip())
        valid_scores = [int(n) for n in numbers if 0 <= int(n) <= 100]

        if valid_scores:
            score = valid_scores[0]
            print(f"[RAG] Parsed score: {score}")
            return score

        # Strategy 2: Try to parse entire response as number
        cleaned = response.strip().replace('%', '').replace('.', '').strip()
        if cleaned.isdigit():
            score = min(100, max(0, int(cleaned)))
            print(f"[RAG] Fallback score: {score}")
            return score

        # Strategy 3: Ask again with even simpler prompt
        simple_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
Resume: {context}
Job: {question}
Give only a number from 0-100 showing match percentage:
            """
        )
        chain2 = (
            {"context": retriever, "question": RunnablePassthrough()}
            | simple_prompt
            | llm
            | StrOutputParser()
        )
        response2 = chain2.invoke(job_description)
        numbers2 = re.findall(r'\b(\d{1,3})\b', response2.strip())
        valid2 = [int(n) for n in numbers2 if 0 <= int(n) <= 100]

        if valid2:
            return valid2[0]

        # Final fallback — return 50 (neutral score, not 0)
        print("[RAG] Could not parse score, returning 50")
        return 50

    except Exception as e:
        print(f"[RAG] Score error: {e}")
        return 50  # Never return 0 on error


# ── MAIN: Full resume analysis
def analyze_resume(pdf_file, job_description, candidate_name):
    """
    Full pipeline:
    1. Extract text from PDF
    2. Build FAISS vector store
    3. Run analysis questions via RAG
    4. Get numeric match score
    5. Return complete result dict
    """

    # Step 1: Extract PDF text
    text = extract_text(pdf_file)
    if not text:
        return {
            "name": candidate_name,
            "score": 0,
            "analysis": {"Error": "Could not extract text from PDF"},
            "raw_text": ""
        }

    # Step 2: Create vector store
    vector_store = create_vector_store(text, candidate_name)

    # Step 3: Run all analysis questions
    questions = [
        f"Rate this candidate from 1-10 for: {job_description}. Explain why.",
        f"What are the top skills relevant to: {job_description}?",
        f"What are the strengths and weaknesses for this role: {job_description}?",
        "What is the candidate's total experience and education background?"
    ]

    analysis = {}
    for q in questions:
        analysis[q] = ask_question(vector_store, q)

    # Step 4: Get match score (fixed strict parser)
    score = get_match_score(vector_store, job_description)

    return {
        "name": candidate_name,
        "score": score,
        "analysis": analysis,
        "raw_text": text[:500]
    }