import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class VectorDB:
    def __init__(self, collection_name: str = "testing_kb"):
        client = chromadb.PersistentClient(path="chroma_db")
        self.collection = client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def chunk_text(self, text: str, source: str, chunk_size: int = 800, overlap: int = 100) -> List[Dict]:
        chunks = []
        start = 0
        text_length = len(text)
        idx = 0
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk_text = text[start:end]
            chunks.append({
                "id": f"{source}_{idx}",
                "text": chunk_text,
                "source": source
            })
            idx += 1
            start += chunk_size - overlap
        return chunks

    def add_documents(self, docs: List[Dict]):
        texts = [d["text"] for d in docs]
        ids = [d["id"] for d in docs]
        metadatas = [{"source": d["source"]} for d in docs]
        embeddings = self.model.encode(texts).tolist()
        self.collection.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)

    def query(self, query_text: str, n_results: int = 5) -> Dict:
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results
