import json

from rag.storage import save_index, load_index
from rag.pipeline import index_file
from rag.semantic_search import search_index_top_k

def test_save_index(tmp_path):
    records = [
        {
            "text": "Customers can request refunds.",
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "vector": [0.5, 0.5]
        }
    ]

    file_path = tmp_path / "embeddings" / "refund_index.json"

    save_index(records, file_path)

    assert file_path.exists()

    with file_path.open("r", encoding="utf-8") as file:
        saved_records = json.load(file)

    assert saved_records == records


def test_load_index(tmp_path):
    records = [
        {
            "text": "Customers can request refunds.",
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "vector": [0.5, 0.5]
        }
    ]

    file_path = tmp_path / "refund_index.json"

    save_index(records, file_path)

    loaded_records = load_index(file_path)

    assert loaded_records == records
    assert loaded_records[0]["vector"] == [0.5, 0.5]


def test_loaded_index_reuses_embeddings(tmp_path):
    calls = []

    def counting_embed(text):
        calls.append(text)
        return [float(len(text)), 0.0]

    indexed_records = index_file(
        file_path="sample_docs/refund_policy.txt",
        chunk_size=8,
        overlap=2,
        embed_fn=counting_embed
    )

    file_path = tmp_path / "refund_index.json"

    save_index(indexed_records, file_path)

    del indexed_records

    calls.clear()

    loaded_records = load_index(file_path)

    results = search_index_top_k(
        "How do refunds work?",
        loaded_records,
        k=2,
        embed_fn=counting_embed
    )

    assert len(results) == 2
    assert calls == ["How do refunds work?"]
    assert results[0]["source"] == "refund_policy.txt"
    assert results[1]["source"] == "refund_policy.txt"