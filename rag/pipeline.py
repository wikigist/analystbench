from rag.documents import chunk_document
from rag.retrieval import retrieve_records_by_keyword
from rag.documents import load_document
from rag.documents import load_document, chunk_document
from rag.semantic_search import index_records
from rag.embeddings import embed_text


def search_document(text, source, keyword, chunk_size=5, overlap=2):
    records = chunk_document(
        text=text,
        source=source,
        chunk_size=chunk_size,
        overlap=overlap
    )

    matches = retrieve_records_by_keyword(records, keyword)

    return matches


def search_file(file_path, keyword, chunk_size=20, overlap=3):
    document = load_document(file_path)

    matches = search_document(
        text=document["text"],
        source=document["source"],
        keyword=keyword,
        chunk_size=chunk_size,
        overlap=overlap
    )

    return matches


def index_file(
    file_path,
    chunk_size=20,
    overlap=3,
    embed_fn=embed_text
):
    document = load_document(file_path)

    records = chunk_document(
        text=document["text"],
        source=document["source"],
        chunk_size=chunk_size,
        overlap=overlap
    )

    indexed_records = index_records(
        records,
        embed_fn=embed_fn
    )

    return indexed_records