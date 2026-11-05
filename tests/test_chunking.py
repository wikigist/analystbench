
from rag.chunking import chunk_text


def test_chunk_text_with_overlap():
    text = "Refunds require a receipt and approval within thirty days."

    chunks = chunk_text(text, chunk_size=5, overlap=2)

    assert chunks == [
        "Refunds require a receipt and",
        "receipt and approval within thirty",
        "within thirty days.",
    ]


def test_chunk_text_with_empty_document():
    assert chunk_text("") == []
