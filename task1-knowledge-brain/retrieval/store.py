"""Chunking + embeddings (Chroma default embedder) + search. Idempotent: chunk ids = url#n."""
import json
import os
import chromadb
from ingestion.crawler import db

client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "..", "chroma"))
col = client.get_or_create_collection("kb_collection")


def chunk(text: str, size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks with early stop on remainder."""
    if not text:
        return []
    chunks = []
    start = 0
    step = max(1, size - overlap)
    while start < len(text):
        chunks.append(text[start : start + size])
        if start + size >= len(text):
            break
        start += step
    return chunks


def index_changed():
    con = db()
    rows = con.execute("SELECT url,title,text,images FROM pages WHERE status='changed'").fetchall()
    for url, title, text, images in rows:
        old = col.get(where={"url": url})
        if old["ids"]:
            col.delete(ids=old["ids"])
        parts = chunk(text or "")
        if parts:
            col.add(
                ids=[f"{url}#{i}" for i in range(len(parts))],
                documents=parts,
                metadatas=[{"url": url, "title": title, "images": images or "[]"} for _ in parts]
            )
        con.execute("UPDATE pages SET status='indexed' WHERE url=?", (url,))
    con.commit()
    print("indexed", len(rows), "pages")


def search(question: str, k: int = 5):
    r = col.query(query_texts=[question], n_results=k)
    if not r["documents"] or not r["documents"][0]:
        return []
    return [
        {"text": d, **m, "images": json.loads(m.get("images") or "[]")}
        for d, m in zip(r["documents"][0], r["metadatas"][0])
    ]


if __name__ == "__main__":
    index_changed()
