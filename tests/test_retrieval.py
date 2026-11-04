from rag.retrieval import retrieve_by_keyword
from rag.retrieval import get_next_chunk
from rag.retrieval import retrieve_records_by_keyword


def test_retrieve_by_keyword():
    chunks = [
        "Customers can request refunds within 30 days.",
        "Employees must complete annual training.",
        "Refund approvals require a receipt."
    ]

    result = retrieve_by_keyword(chunks, "refund")

    assert len(result) == 2
    assert result == [
    "Customers can request refunds within 30 days.",
    "Refund approvals require a receipt."
    ]


def test_get_next_chunk():
    chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]

    assert get_next_chunk(chunks, 1) == "Chunk 3"
    assert get_next_chunk(chunks, 2) is None


def test_retrieve_records_preserves_metadata():
    records = [
        {
            "text": "Refunds require a receipt",
            "source": "refund_policy.txt",
            "chunk_id": 0
        },
        {
            "text": "Employees complete training",
            "source": "staff_policy.txt",
            "chunk_id": 0
        }
    ]

    result = retrieve_records_by_keyword(records, "refund")

    assert result == [records[0]]