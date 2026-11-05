from rag.pipeline import search_document
from rag.pipeline import search_file


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