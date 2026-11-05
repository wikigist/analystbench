from rag.documents import chunk_document


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