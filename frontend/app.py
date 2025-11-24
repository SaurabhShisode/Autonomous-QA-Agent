import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")
st.title("Autonomous QA Agent for Test Case and Script Generation")

if "generated_test_cases" not in st.session_state:
    st.session_state.generated_test_cases = ""

st.sidebar.header("Configuration")
backend_url = st.sidebar.text_input("Backend URL", API_BASE)

st.header("Phase 1: Upload Documents and HTML")
uploaded_files = st.file_uploader(
    "Upload support documents and checkout.html",
    accept_multiple_files=True,
    type=["pdf", "md", "txt", "json", "html", "htm"],
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Upload and Index"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            files_payload = []
            for f in uploaded_files:
                files_payload.append(("files", (f.name, f.getvalue(), f.type)))
            try:
                resp = requests.post(f"{backend_url}/upload_documents", files=files_payload)
                data = resp.json()
                chunks = data.get("chunks_indexed", 0)
                st.success(f"Documents uploaded successfully. Chunks indexed: {chunks}")
            except Exception as e:
                st.error(f"Error contacting backend: {e}")

with col2:
    if st.button("Build Knowledge Base"):
        try:
            resp = requests.post(f"{backend_url}/build_kb")
            st.success(resp.json().get("message", "Knowledge base ready"))
        except Exception as e:
            st.error(f"Error contacting backend: {e}")

st.markdown("---")

st.header("Phase 2: Generate Test Cases")

query = st.text_input(
    "Describe what test cases you want",
    "Generate all positive and negative test cases for the discount code feature."
)

if st.button("Generate Test Cases"):
    try:
        resp = requests.post(f"{backend_url}/generate_test_cases", data={"query": query})
        data = resp.json()
        st.session_state.generated_test_cases = data.get("raw_output", "No output")
    except Exception as e:
        st.error(f"Error contacting backend: {e}")

if st.session_state.generated_test_cases:
    st.subheader("Raw Test Case Output")
    st.markdown(st.session_state.generated_test_cases)


st.markdown("---")

st.header("Phase 3: Generate Selenium Script")

phase3_test_case = st.text_area("Paste or type one selected test case from the above output")

if st.button("Generate Selenium Script"):
    try:
        data = {
            "test_case_text": phase3_test_case
        }
        resp = requests.post(f"{backend_url}/generate_script", data=data)
        st.subheader("Generated Selenium Script")
        st.code(resp.json().get("script", "No script generated"))
    except Exception as e:
        st.error(f"Error contacting backend: {e}")
