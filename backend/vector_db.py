import uuid
from typing import List, Dict, Any

import chromadb
from sentence_transformers import SentenceTransformer


class VectorDB:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.html_sources: Dict[str, str] = {}

    def chunk_text(self, text: str, source: str) -> List[Dict[str, str]]:
        chunks: List[Dict[str, str]] = []
        chunk_size = 800
        overlap = 200
        start = 0
        length = len(text)
        while start < length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append({"text": chunk, "source": source})
            start += chunk_size - overlap
        return chunks

    def add_documents(self, chunks: List[Dict[str, str]]) -> None:
        if not chunks:
            return
        ids: List[str] = []
        docs: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        for chunk in chunks:
            ids.append(str(uuid.uuid4()))
            docs.append(chunk["text"])
            metadatas.append({"source": chunk["source"]})
        self.collection.add(ids=ids, documents=docs, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 8) -> Dict[str, Any]:
        embedding = self.embedder.encode([query_text]).tolist()
        return self.collection.query(query_embeddings=embedding, n_results=n_results)

    def store_html_source(self, filename: str, text: str) -> None:
        self.html_sources[filename] = text

    def get_html_source(self, filename: str) -> str:
        return self.html_sources.get(filename, "")

    def get_first_html_source(self) -> str:
        if not self.html_sources:
            return ""
        return next(iter(self.html_sources.values()))
