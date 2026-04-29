# ============================================================
# GRAPH BUILDER — Knowledge graph using Neo4j + Groq LLM
# ============================================================

import os
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ── Initialize Neo4j driver with error handling
_driver = None

def get_driver():
    """
    Get Neo4j driver — only connect if env vars are set.
    Returns None if Neo4j is not configured.
    """
    global _driver
    if _driver is not None:
        return _driver

    uri      = os.getenv("NEO4J_URI", "")
    password = os.getenv("NEO4J_PASSWORD", "")

    if not uri or not password:
        print("[Graph] Neo4j not configured — skipping DB push")
        return None

    try:
        _driver = GraphDatabase.driver(uri, auth=("neo4j", password))
        # Test connection
        _driver.verify_connectivity()
        print("[Graph] Neo4j connected successfully")
        return _driver
    except Exception as e:
        print(f"[Graph] Neo4j connection failed: {e}")
        return None


# ── CORE: Extract graph data from resume text using LLM
def extract_graph_data(text):
    """
    Ask Groq LLM to extract nodes and edges from resume.
    Returns valid graph dict with nodes + edges.

    FIX: Added strict JSON cleanup and fallback on parse error.
    """
    # Use only first 3000 chars to avoid token limits
    text_snippet = text[:3000]

    prompt = ChatPromptTemplate.from_template("""
Extract entities and relationships from this resume.
Return ONLY valid JSON — no markdown, no explanation, no code blocks.

Required format:
{{
    "nodes": [
        {{"id": "PersonName", "label": "Person"}},
        {{"id": "SkillName", "label": "Technology"}},
        {{"id": "CompanyName", "label": "Organization"}},
        {{"id": "ProjectName", "label": "Project"}},
        {{"id": "DegreeName", "label": "Education"}}
    ],
    "edges": [
        {{"source": "PersonName", "target": "SkillName", "type": "HAS_SKILL"}},
        {{"source": "PersonName", "target": "CompanyName", "type": "WORKED_AT"}},
        {{"source": "PersonName", "target": "ProjectName", "type": "BUILT"}},
        {{"source": "PersonName", "target": "DegreeName", "type": "STUDIED"}}
    ]
}}

Resume:
{text}
    """)

    try:
        chain    = prompt | llm
        response = chain.invoke({"text": text_snippet})
        raw      = response.content.strip()

        print(f"[Graph] Raw LLM response (first 200): {raw[:200]}")

        # FIX: Clean markdown code blocks if LLM adds them
        raw = raw.replace("```json", "").replace("```", "").strip()

        # FIX: Find JSON object in response even if extra text exists
        start = raw.find('{')
        end   = raw.rfind('}') + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        graph_data = json.loads(raw)

        # Validate structure
        if "nodes" not in graph_data:
            graph_data["nodes"] = []
        if "edges" not in graph_data:
            graph_data["edges"] = []

        print(f"[Graph] Extracted {len(graph_data['nodes'])} nodes, {len(graph_data['edges'])} edges")
        return graph_data

    except json.JSONDecodeError as e:
        print(f"[Graph] JSON parse error: {e}")
        # Return minimal graph on parse failure
        return _minimal_graph(text_snippet)

    except Exception as e:
        print(f"[Graph] LLM extraction error: {e}")
        return _minimal_graph(text_snippet)


def _minimal_graph(text):
    """
    Fallback graph — extract basic info from text
    when LLM fails to return valid JSON.
    """
    # Try to find a name (first line usually has name)
    lines  = [l.strip() for l in text.split('\n') if l.strip()]
    name   = lines[0] if lines else "Candidate"

    # Extract capitalized words as tech nodes
    import re
    tech_words = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text)
    tech_nodes = list(set(tech_words[:10]))  # Max 10 tech nodes

    nodes = [{"id": name, "label": "Person"}]
    edges = []

    for tech in tech_nodes:
        if tech not in ["The", "This", "That", "With", "From", "Have"]:
            nodes.append({"id": tech, "label": "Technology"})
            edges.append({"source": name, "target": tech, "type": "HAS_SKILL"})

    return {"nodes": nodes, "edges": edges}


# ── UTILITY: Push graph data to Neo4j
def push_to_neo4j(graph_data, candidate_name):
    """
    Store nodes and edges in Neo4j.
    Skips silently if Neo4j is not connected.
    """
    driver = get_driver()
    if not driver:
        return  # Neo4j not available — skip, don't crash

    try:
        with driver.session() as session:

            # Clear old data for this candidate
            session.run(
                "MATCH (n {candidate: $name}) DETACH DELETE n",
                name=candidate_name
            )

            # Create all nodes
            for node in graph_data.get("nodes", []):
                session.run(
                    f"MERGE (n:{node['label']} {{id: $id, candidate: $candidate}})",
                    id=node["id"],
                    candidate=candidate_name
                )

            # Create all relationships
            for edge in graph_data.get("edges", []):
                session.run(
                    "MATCH (a {id: $source}), (b {id: $target}) "
                    f"MERGE (a)-[r:{edge['type']}]->(b)",
                    source=edge["source"],
                    target=edge["target"]
                )

        print(f"[Graph] Neo4j updated for: {candidate_name}")

    except Exception as e:
        print(f"[Graph] Neo4j push error: {e}")
        # Don't crash the app — graph is optional


# ── MAIN: Build knowledge graph
def build_knowledge_graph(text, candidate_name):
    """
    Full pipeline:
    1. Extract nodes + edges from resume text using LLM
    2. Push to Neo4j (if available)
    3. Return graph data for frontend visualization
    """
    # Step 1: Extract graph data
    graph_data = extract_graph_data(text)

    # Step 2: Push to Neo4j (won't crash if unavailable)
    push_to_neo4j(graph_data, candidate_name)

    # Step 3: Always return graph data for SVG visualization
    return graph_data