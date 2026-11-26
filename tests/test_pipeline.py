from rag.pipeline import search_document
from rag.pipeline import search_file
from rag.pipeline import index_file
from rag.semantic_search import search_index_top_k
from rag.pipeline import answer_from_index


def test_search_document_returns_evidence_with_source():
    result = search_document(
        text="Refunds are allowed within thirty days. Employees must complete annual training.",
        source="refund_policy.txt",
        keyword="refund",
        chunk_size=6,
        overlap=1
    )

    assert result == [
        {
            "text": "Refunds are allowed within thirty days.",
            "source": "refund_policy.txt",
            "chunk_id": 0
        }
    ]


def test_search_file_returns_source():
    results = search_file(
        file_path="sample_docs/refund_policy.txt",
        keyword="refund",
        chunk_size=20,
        overlap=3
    )

    assert len(results) > 0
    assert results[0]["source"] == "refund_policy.txt"
    assert "refund" in results[0]["text"].lower()


def test_chunk_size_changes_retrieved_evidence():
    small_matches = search_file(
        file_path="sample_docs/refund_policy.txt",
        keyword="refund",
        chunk_size=4,
        overlap=0
    )

    large_matches = search_file(
        file_path="sample_docs/refund_policy.txt",
        keyword="refund",
        chunk_size=20,
        overlap=3
    )

    assert "thirty days" not in small_matches[0]["text"].lower()

    assert "thirty days" in large_matches[0]["text"].lower()


def test_index_file_preserves_source_and_embeddings():
    def fake_embed(text):
        return [float(len(text)), 0.0]

    indexed_records = index_file(
        file_path="sample_docs/refund_policy.txt",
        chunk_size=20,
        overlap=3,
        embed_fn=fake_embed
    )

    assert len(indexed_records) > 0
    assert indexed_records[0]["source"] == "refund_policy.txt"
    assert indexed_records[0]["chunk_id"] == 0

    assert indexed_records[0]["vector"] == [
        float(len(indexed_records[0]["text"])),
        0.0
    ]


def test_search_indexed_file_returns_source_chunks():
    def fake_embed(text):
        return [float(len(text)), 0.0]

    indexed_records = index_file(
        file_path="sample_docs/refund_policy.txt",
        chunk_size=8,
        overlap=2,
        embed_fn=fake_embed
    )

    results = search_index_top_k(
        "How do refunds work?",
        indexed_records,
        k=2,
        embed_fn=fake_embed
    )

    assert len(results) == 2
    assert results[0]["source"] == "refund_policy.txt"
    assert results[1]["source"] == "refund_policy.txt"
    assert "chunk_id" in results[0]



def test_indexed_file_reuses_embeddings():
    calls = []

    def counting_embed(text):
        calls.append(text)
        return [float(len(text)), 0.0]

    indexed_records = index_file(
        file_path="sample_docs/refund_policy.txt",
        chunk_size=20,
        overlap=3,
        embed_fn=counting_embed
    )

    document_calls = len(calls)

    assert document_calls == len(indexed_records)

    search_index_top_k(
        "How do refunds work?",
        indexed_records,
        k=2,
        embed_fn=counting_embed
    )

    assert len(calls) == document_calls + 1


def test_answer_from_index_retrieves_and_generates():
    question = "How long is the refund period?"

    indexed_records = [
        {
            "source": "delivery_policy.txt",
            "chunk_id": 0,
            "text": "Delivery takes 5 days.",
            "vector": [0.0, 1.0]
        },
        {
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "text": "Refunds within 30 days.",
            "vector": [1.0, 0.0]
        }
    ]

    def fake_embed(text):
        return [1.0, 0.0]

    received_prompts = []

    def fake_generate(prompt):
        received_prompts.append(prompt)
        return "Customers have 30 days to request a refund."

    answer = answer_from_index(
        question,
        indexed_records,
        fake_generate,
        k=1,
        embed_fn=fake_embed
    )

    assert answer == "Customers have 30 days to request a refund."
    assert len(received_prompts) == 1

    assert "[refund_policy.txt:0] Refunds within 30 days." in received_prompts[0]
    assert "Delivery takes 5 days." not in received_prompts[0]
    assert f"Question: {question}" in received_prompts[0]


def test_answer_from_index_abstains_with_empty_index():
    question = "How long is the refund period?"
    indexed_records = []

    def fake_embed(text):
        raise AssertionError("Embedding should not be called")

    def fake_generate(prompt):
        raise AssertionError("Generator should not be called")

    answer = answer_from_index(
        question,
        indexed_records,
        fake_generate,
        k=1,
        embed_fn=fake_embed
    )

    assert answer == "I don't know."