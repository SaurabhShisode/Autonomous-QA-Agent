# Autonomous QA Agent

AI-powered Test Case Generator and Selenium Script Writer

This project implements an autonomous QA testing assistant capable of:

1. **Reading and understanding product documentation (PDF, HTML, JSON, TXT, MD).**
2. **Generating high quality functional test cases using RAG (Retrieval Augmented Generation).**
3. **Generating Selenium automation scripts from user selected test cases.**

The system follows a strict architecture described in the assignment and combines **FastAPI**, **Chroma Vector Database**, **Sentence Transformers embeddings**, and **Groq LLM** to automatically produce consistent, grounded QA output.

---

## **1. How the System Works**

The system works in 3 clearly defined phases:

---

## **Phase 1. Document Upload and Knowledge Base Construction**

Users upload any of the following:

- Product specification PDFs
- Test plans
- Requirement documents
- HTML UI source (checkout.html)
- JSON config files
- Markdown or plain text files

The backend:

- Extracts text from files (PDF, HTML, JSON)
- Splits content into overlapping chunks
- Embeds chunks using **sentence-transformers all-MiniLM-L6-v2**
- Stores embeddings in **ChromaDB** for retrieval

The result:  
A complete **context-aware knowledge base** grounded only in what the user uploads.

---

## **Phase 2. Test Case Generation**

Users type a query such as:

> Generate all positive and negative test cases for discount code validation.

The backend:

1. Searches ChromaDB for relevant text chunks  
2. Sends retrieved chunks + user query to the Groq LLM  
3. LLM generates test cases in **Markdown table format**

The Streamlit UI displays the raw Markdown directly.

Users review the test cases and select one scenario for script generation.

---

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

---

# **2. System Architecture**

```
                 DOCUMENT UPLOAD
                          |
                          V
        ┌──────────────────────────┐
        │   Text Extraction Layer  │
        └──────────────────────────┘
          | PDF, HTML, JSON Parsing
          V
        ┌──────────────────────────┐
        │   Chunking + Embedding   │
        └──────────────────────────┘
          | Sentence Transformers
          V
        ┌──────────────────────────┐
        │     Chroma Vector DB     │
        └──────────────────────────┘
                          |
                          |
         =============================
                Phase 2 Query
         =============================
                          |
                          V
            Retrieve Relevant Chunks
                          |
                          V
          LLM Generates Test Cases
                          |
                          V
        User Selects One Test Case
                          |
                          |
         =============================
                Phase 3 Generation
         =============================
                          |
                          V
  LLM Reads: HTML + Context + Test Case
                          |
                          V
        Generates Selenium Script
```

---

# **3. Features**

### ✔ Upload multiple document formats

PDF, TXT, JSON, MD, HTML

### ✔ Automatic text extraction

PyMuPDF for PDF, BeautifulSoup for HTML, JSON prettifier

### ✔ Smart chunking and embeddings

Overlap based chunking for better semantic recall

### ✔ AI based test case generation

Markdown table format

### ✔ AI based Selenium script generation

Scripts grounded in uploaded HTML

### ✔ Clean Streamlit UI

3 phase workflow matching assignment instructions

### ✔ FastAPI backend + Streamlit frontend separation

---

# **4. Tech Stack**

### **Frontend**

- Streamlit
- Requests

### **Backend**

- FastAPI
- Uvicorn
- Groq LLM API
- ChromaDB
- Sentence Transformers
- PyMuPDF
- BeautifulSoup

---

# **5. Setup Instructions**

## **Backend Setup**

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

---

## **Frontend Setup**

```bash
cd frontend
streamlit run app.py
```

---

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


