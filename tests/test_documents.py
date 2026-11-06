from rag.documents import chunk_document
from rag.documents import load_document


def test_chunk_document_preserves_metadata():
    records = chunk_document(
        text="Refunds require a receipt and approval",
        source="refund_policy.txt",
        chunk_size=4,
        overlap=1
    )

    assert records == [
        {
            "text": "Refunds require a receipt",
            "source": "refund_policy.txt",
            "chunk_id": 0
        },
        {
            "text": "receipt and approval",
            "source": "refund_policy.txt",
            "chunk_id": 1
        }
    ]

def test_load_document():
    document = load_document("sample_docs/refund_policy.txt")

    assert document["source"] == "refund_policy.txt"
    assert "Customers can request refunds" in document["text"]