from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from parser import extract_text
from vector_db import VectorDB
from rag_testcase_agent import generate_test_cases
from rag_script_agent import generate_selenium_script

app = FastAPI()
db = VectorDB()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    all_chunks = []
    for uploaded in files:
        content = await uploaded.read()
        text = extract_text(uploaded.filename, content)
        chunks = db.chunk_text(text, uploaded.filename)
        all_chunks.extend(chunks)

    if all_chunks:
        db.add_documents(all_chunks)

    return {"status": "ok", "chunks_indexed": len(all_chunks)}

@app.post("/build_kb")
async def build_kb():
    return {"status": "ok", "message": "Knowledge base built"}


@app.post("/generate_test_cases")
async def api_generate_test_cases(query: str = Form(...)):
    result = generate_test_cases(db, query)
    return result

@app.post("/generate_script")
async def api_generate_script(test_case_text: str = Form(...)):
    result = generate_selenium_script(db, test_case_text)
    return {"script": result.get("raw_output", "")}
