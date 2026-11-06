from rag.chunking import chunk_text
from pathlib import Path


def chunk_document(text, source, chunk_size=5, overlap=2):
    text_chunks = chunk_text(text, chunk_size, overlap)

    records = []

    for chunk_id, chunk in enumerate(text_chunks):
        records.append({
            "text": chunk,
            "source": source,
            "chunk_id": chunk_id
        })

    return records


def load_document(file_path):
    path = Path(file_path)

    text = path.read_text(encoding="utf-8")

    return {
        "text": text,
        "source": path.name
    }