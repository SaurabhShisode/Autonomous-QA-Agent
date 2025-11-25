# Autonomous QA Agent

AI-powered Test Case Generator and Selenium Script Writer

This repository provides an end-to-end autonomous QA assistant that:
- Reads and understands product documentation (PDF, HTML, JSON, TXT, Markdown)
- Builds a grounded knowledge base using Retrieval-Augmented Generation (RAG)
- Generates functional positive, negative, and edge-case test cases
- Produces Selenium Python scripts strictly grounded in uploaded HTML

The system uses a three-phase workflow with a FastAPI backend and a Streamlit frontend. Key components include ChromaDB, Sentence Transformers, and the Groq LLM.



## 1. How the Agent Works

The workflow runs in three phases.


This produces a grounded, queryable knowledge base for all subsequent LLM generations.

### Phase 2 — Test Case Generation
1. User submits a request (example: “Generate all positive and negative test cases for the discount code feature.”)  
2. Backend retrieves relevant knowledge chunks from ChromaDB  
3. The user query plus retrieved context is sent to the Groq LLM  
4. The LLM returns structured test cases, presented in Markdown table format in the Streamlit UI

Users review the test cases and select one scenario for script generation.

### Phase 3 — Selenium Script Generation
When a test case is selected (pasted into the UI), the backend:
1. Retrieves related context from ChromaDB  
2. Loads the uploaded HTML (e.g., `checkout.html`) and extracts the DOM structure  
3. Sends the HTML content, DOM, relevant context, and the selected test case to the LLM

The LLM generates a Selenium Python script that:
- Is grounded in the real HTML
- Uses only valid selectors from the provided DOM
- Matches the selected test scenario
- Avoids hallucinated IDs or elements

The generated script is displayed in Streamlit and can be executed by the user.



## 2. System Architecture Overview

> Generate all positive and negative test cases for discount code validation.

The backend:

1. Searches ChromaDB for relevant text chunks  
2. Sends retrieved chunks + user query to the Groq LLM  
3. LLM generates test cases in **Markdown table format**

The Streamlit UI displays the raw Markdown directly.

Users then manually **copy any one test case** and paste it into Phase 3.



## **Phase 3. Selenium Script Generation**

Users paste one selected test case into a text box.

The backend:

1. Retrieves relevant context again from ChromaDB  
2. Loads the uploaded checkout.html  
3. Sends:
    - HTML source
    - Test case text
    - Annotated context  
    to the LLM
4. Model produces a **fully grounded Selenium Python script**
    - Uses only real locators from the provided HTML
    - No invented IDs
    - Aligned to the selected test case

The Streamlit UI shows the generated script cleanly formatted.



# **2. System Architecture**

```
                 ┌──────────────────────────┐
                 │      DOCUMENT UPLOAD     │
                 └──────────────────────────┘
                               |
                               V
        ┌───────────────────────────────────────────┐
        │        Text Extraction + Preprocessing    │
        └───────────────────────────────────────────┘
                               |
                               V
        ┌───────────────────────────────────────────┐
        │       Chunking + Sentence Embeddings      │
        └───────────────────────────────────────────┘
                               |
                               V
        ┌───────────────────────────────────────────┐
        │          Chroma Vector Database           │
        └───────────────────────────────────────────┘
                               |
             =====================================
                            Phase 2 Query
             =====================================
                               |
                               V
                 Retrieve Relevant Chunks
                               |
                               V
                 LLM Generates Test Cases
                               |
                               V
               User Selects a Single Test Case
                               |
                =====================================
                        Phase 3 Script Gen
                =====================================
                               |
                               V
        LLM Reads HTML + Test Case + Context → Script
```



## 3. Key Features

Document handling
- Supports PDF, HTML, Markdown, JSON, and plain text
- Automatic extraction, cleaning, and chunking
- HTML DOM parsing for reliable locator extraction

RAG-based test case generator
- Semantic search via ChromaDB
- Structured Markdown output (tables)
- Positive, negative, and edge-case tests

Selenium script generator
- Python Selenium script output
- Grounded only in the uploaded UI HTML (no hallucinated locators)
- Clear step-by-step action mapping

User interface
- Clear three-phase workflow in Streamlit
- Simple document upload, immediate generation of test cases and scripts



## 4. Tech Stack

### ✔ AI based Selenium script generation

Scripts grounded in uploaded HTML

### ✔ Clean Streamlit UI

3 phase workflow matching assignment instructions

### ✔ FastAPI backend + Streamlit frontend separation



# **4. Tech Stack**

### **Frontend**

- Streamlit
- Requests

### **Backend**

- FastAPI
- Uvicorn
- Groq LLM API
- ChromaDB
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Groq LLM API
- PyMuPDF (PDF extraction)
- BeautifulSoup (HTML parsing)




## 5. Setup Instructions

Prerequisites: Python 3.10+

Backend
```bash
cd backend
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate
pip install -r requirements.txt
```

Run backend:
```bash
uvicorn main:app --reload --port 8000
```



## **Frontend Setup**

```bash
cd frontend
streamlit run app.py
```



# **6. Usage Guide**

### **Phase 1: Upload Files**

1. Select PDFs, HTML, JSON, or text files  
2. Click **Upload and Index**  
3. Click **Build Knowledge Base**

### **Phase 2: Generate Test Cases**

1. Enter a query like  
    "Generate all test cases for login validation"  
2. Click **Generate Test Cases**  
3. Test cases appear in Markdown format  
4. Copy one test case

### **Phase 3: Selenium Script Generation**

1. Paste one selected test case  
2. Click **Generate Selenium Script**  
3. Script appears in a code block


## 6. Usage Guide

Phase 1 — Upload & Index
1. Upload PDFs, HTML, JSON, or text files  
2. Click “Upload and Index”  
3. Click “Build Knowledge Base”

Phase 2 — Generate Test Cases
1. Enter a query (e.g., "Generate test cases for login validation")  
2. Click “Generate Test Cases”  
3. Review Markdown table output  
4. Copy one test case scenario for script generation

Phase 3 — Generate Selenium Script
1. Paste the selected test case into the UI  
2. Click “Generate Selenium Script”  
3. The generated Python Selenium script appears formatted in the UI



## 7. Supported Document Formats

| Format | Purpose                                       |
| ------ | --------------------------------------------- |
| PDF    | Requirement docs, SRS, functional flows       |
| HTML   | UI structure for generating grounded locators |
| JSON   | Product configuration, button mapping         |
| TXT/MD | Notes, descriptions, instructions             |

These uploaded documents are the basis for both test cases and automation scripts. All outputs are strictly grounded in the provided content.

