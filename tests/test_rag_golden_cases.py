import json
from rag.semantic_search import search_index_top_k
from rag.retrieval_eval import evaluate_retrieved_chunks

from rag.pipeline import index_file


def test_refund_deadline_gold_label():
    with open(
        "benchmarks/rag_retrieval_cases.json",
        encoding="utf-8"
    ) as file:
        cases = json.load(file)

    case = cases[0]

    def fake_embed(text):
        return [float(len(text)), 0.0]

    records = index_file(
        file_path=case["file_path"],
        chunk_size=case["chunk_size"],
        overlap=case["overlap"],
        embed_fn=fake_embed
    )

    expected = case["relevant_records"][0]

    matching_chunks = [
        record
        for record in records
        if record["source"] == expected["source"]
        and record["chunk_id"] == expected["chunk_id"]
    ]

    assert len(matching_chunks) == 1
    assert "thirty days" in matching_chunks[0]["text"].lower()


def test_refund_deadline_retrieval_evaluation():
    with open(
        "benchmarks/rag_retrieval_cases.json",
        encoding="utf-8"
    ) as file:
        cases = json.load(file)

    case = cases[0]

    def fake_embed(text):
        text = text.lower()

        if "how long" in text or "thirty days" in text:
            return [1.0, 0.0]

        return [0.0, 1.0]

    records = index_file(
        file_path=case["file_path"],
        chunk_size=case["chunk_size"],
        overlap=case["overlap"],
        embed_fn=fake_embed
    )

    retrieved = search_index_top_k(
        case["question"],
        records,
        k=2,
        embed_fn=fake_embed
    )

    result = evaluate_retrieved_chunks(
        retrieved,
        case["relevant_records"],
        k=2
    )

    assert result["recall"] == 1.0
    assert result["precision"] == 0.5