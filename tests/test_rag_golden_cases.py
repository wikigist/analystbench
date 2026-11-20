import json
from rag.semantic_search import search_index_top_k
from rag.retrieval_eval import evaluate_retrieved_chunks
from rag.golden_eval import evaluate_golden_cases

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



def test_all_golden_case_labels_exist():
    with open(
        "benchmarks/rag_retrieval_cases.json",
        encoding="utf-8"
    ) as file:
        cases = json.load(file)

    def fake_embed(text):
        return [float(len(text)), 0.0]

    for case in cases:
        records = index_file(
            file_path=case["file_path"],
            chunk_size=case["chunk_size"],
            overlap=case["overlap"],
            embed_fn=fake_embed
        )

        for expected in case["relevant_records"]:
            matching_chunks = [
                record
                for record in records
                if record["source"] == expected["source"]
                and record["chunk_id"] == expected["chunk_id"]
            ]

            assert len(matching_chunks) == 1
            assert expected["evidence_phrase"] in matching_chunks[0]["text"].lower()


def test_evaluate_multiple_golden_cases():
    with open(
        "benchmarks/rag_retrieval_cases.json",
        encoding="utf-8"
    ) as file:
        cases = json.load(file)

        embedded_texts = []

    def fake_embed(text):
        embedded_texts.append(text)
        text = text.lower()

        if "how long" in text or "thirty days" in text:
            return [1.0, 0.0]

        if "receipt" in text:
            return [0.0, 1.0]

        return [-1.0, -1.0]

    results = evaluate_golden_cases(
        cases,
        embed_fn=fake_embed,
        k=1
    )

    assert [result["case_id"] for result in results] == [
        "RAG001",
        "RAG002"
    ]

    assert all(result["recall"] == 1.0 for result in results)
    assert all(result["precision"] == 1.0 for result in results)
    assert [result["retrieved_chunk_ids"] for result in results] == [
    [1],
    [2]
    ]
    assert len(embedded_texts) == 7


def test_changed_document_is_reindexed(tmp_path):
    file_path = tmp_path / "refund_policy.txt"

    file_path.write_text("Refunds within 30 days.")

    cases = [
        {
            "case_id": "TEST001",
            "file_path": str(file_path),
            "chunk_size": 20,
            "overlap": 2,
            "question": "Question one?",
            "relevant_records": []
        },
        {
            "case_id": "TEST002",
            "file_path": str(file_path),
            "chunk_size": 20,
            "overlap": 2,
            "question": "Question two?",
            "relevant_records": []
        }
    ]

    print("Case IDs:", [case["case_id"] for case in cases])

    embedding_calls = []

    def fake_embed(text):
        embedding_calls.append(text)

        if text == "Question one?":
            file_path.write_text("Refunds within 60 days.")

        return [float(len(text)), 0.0]

    results = evaluate_golden_cases(
        cases,
        embed_fn=fake_embed,
        k=1
    )

    assert len(results) == 2

    assert embedding_calls == [
        "Refunds within 30 days.",
        "Question one?",
        "Refunds within 60 days.",
        "Question two?"
        ]