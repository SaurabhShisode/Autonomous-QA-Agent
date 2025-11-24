from typing import Dict, List
from vector_db import VectorDB
from llm_client import generate_completion_with_system


def build_script_prompt(context_chunks: List[str], test_case_text: str, html_source: str) -> str:
    context_text = "\n\n".join(context_chunks)
    user_prompt = (
        "You are an expert QA automation engineer.\n"
        "You write Selenium Python code that is fully grounded in the provided HTML source.\n"
        "Use only locators that exist in the HTML. Do not invent ids or classes.\n"
        "Return only Python code for a Selenium test, no explanations.\n\n"
        "HTML source:\n"
        f"{html_source}\n\n"
        "Context documents:\n"
        f"{context_text}\n\n"
        "Test case to automate:\n"
        f"{test_case_text}\n\n"
        "Now generate the Selenium test code."
    )
    system_prompt = "You generate robust Selenium Python scripts grounded in the provided HTML and documentation."
    return generate_completion_with_system(system_prompt, user_prompt)


def generate_selenium_script(db: VectorDB, test_case_text: str) -> Dict:
    results = db.query(test_case_text, n_results=8)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    context_chunks: List[str] = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "unknown")
        annotated = f"Source: {source}\n{doc}"
        context_chunks.append(annotated)
    html_source = db.get_first_html_source()
    output = build_script_prompt(context_chunks, test_case_text, html_source)
    return {"raw_output": output}
