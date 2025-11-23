from typing import Dict, List
from vector_db import VectorDB
from llm_client import generate_completion_with_system

def build_testcase_prompt(context_chunks: List[str], user_query: str) -> str:
    context_text = "\n\n".join(context_chunks)
    user_prompt = (
        "You are a QA test engineer.\n"
        "You must generate test cases strictly based on the provided context.\n"
        "Do not invent features that are not mentioned.\n"
        "Return the test cases in Markdown table format with columns:\n"
        "Test_ID, Feature, Test_Scenario, Test_Steps, Expected_Result, Grounded_In.\n"
        "Grounded_In should name the source document file.\n\n"
        "Context:\n"
        f"{context_text}\n\n"
        "User request:\n"
        f"{user_query}\n\n"
        "Now produce the table."
    )
    system_prompt = "You generate structured QA test cases that are fully grounded in the provided documentation."
    return generate_completion_with_system(system_prompt, user_prompt)

def generate_test_cases(db: VectorDB, query_text: str) -> Dict:
    results = db.query(query_text, n_results=8)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    context_chunks = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "unknown")
        annotated = f"Source: {source}\n{doc}"
        context_chunks.append(annotated)
    output = build_testcase_prompt(context_chunks, query_text)
    return {"raw_output": output}
