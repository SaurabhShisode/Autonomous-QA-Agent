import fitz
from bs4 import BeautifulSoup
import json
import io

def extract_text(filename: str, content: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        return extract_pdf_text(content)
    if filename.lower().endswith(".html") or filename.lower().endswith(".htm"):
        return extract_html_text(content)
    if filename.lower().endswith(".json"):
        return extract_json_text(content)
    return content.decode("utf-8", errors="ignore")

def extract_pdf_text(content: bytes) -> str:
    text = ""
    file_stream = io.BytesIO(content)
    doc = fitz.open(stream=file_stream, filetype="pdf")
    for page in doc:
        text += page.get_text()
        text += "\n"
    return text

def extract_html_text(content: bytes) -> str:
    html = content.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator=" ")
    return text

def extract_json_text(content: bytes) -> str:
    data = json.loads(content.decode("utf-8", errors="ignore"))
    return json.dumps(data, indent=2)
