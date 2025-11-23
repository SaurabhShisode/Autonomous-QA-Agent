import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")
st.title("Autonomous QA Agent for Test Case and Script Generation")

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
                st.write(resp.json())
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

query = st.text_input("Describe what test cases you want", "Generate all positive and negative test cases for the discount code feature.")

if st.button("Generate Test Cases"):
    try:
        resp = requests.post(f"{backend_url}/generate_test_cases", data={"query": query})
        data = resp.json()
        st.subheader("Raw Test Case Output")
        st.markdown(data.get("raw_output", "No output"))
    except Exception as e:
        st.error(f"Error contacting backend: {e}")

st.markdown("---")
st.header("Phase 3: Generate Selenium Script")

test_case_text = st.text_area("Paste or type one selected test case from the above output")
feature_query = st.text_input("Feature or keyword to retrieve relevant docs again", "discount code")
html_source = st.text_area("Paste the full checkout.html source here")

if st.button("Generate Selenium Script"):
    if not test_case_text or not html_source:
        st.warning("Please provide test case text and HTML source.")
    else:
        try:
            resp = requests.post(
                f"{backend_url}/generate_script",
                data={
                    "test_case_text": test_case_text,
                    "feature_query": feature_query,
                    "html_source": html_source,
                },
            )
            data = resp.json()
            st.subheader("Generated Selenium Python Script")
            st.code(data.get("raw_output", "No script output"), language="python")
        except Exception as e:
            st.error(f"Error contacting backend: {e}")
