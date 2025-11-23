from typing import Dict, List
from vector_db import VectorDB
from llm_client import generate_completion_with_system

def build_script_prompt(test_case_text: str, html_source: str, context_chunks: List[str]) -> str:
    context_text = "\n\n".join(context_chunks)
    user_prompt = (
        "You are an expert Python Selenium engineer.\n"
        "You must write a complete Selenium script in Python for the given test case.\n"
        "Use only locators that exist in the provided HTML.\n"
        "Prefer id, name and simple CSS selectors.\n"
        "Include basic assertions that match the Expected_Result from the test case.\n"
        "Do not invent UI elements that are not in the HTML.\n\n"
        "Relevant documentation context:\n"
        f"{context_text}\n\n"
        "Checkout HTML:\n"
        f"{html_source}\n\n"
        "Selected Test Case:\n"
        f"{test_case_text}\n\n"
        "Return only Python code inside a single code block."
    )
    system_prompt = "You create clean, runnable Selenium Python scripts that are strictly aligned with the given HTML and documentation."
    return generate_completion_with_system(system_prompt, user_prompt)

def generate_selenium_script(db: VectorDB, test_case_text: str, feature_query: str, html_source: str) -> Dict:
    results = db.query(feature_query, n_results=6)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    context_chunks = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "unknown")
        annotated = f"Source: {source}\n{doc}"
        context_chunks.append(annotated)
    output = build_script_prompt(test_case_text, html_source, context_chunks)
    return {"raw_output": output}
