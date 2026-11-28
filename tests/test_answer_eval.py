from rag.answer_eval import extract_citations
from rag.answer_eval import extract_citations, validate_citations


def test_extract_citations_multiple():
    answer = (
        "Refunds within 30 days [refund_policy.txt:0]. "
        "A receipt is required [refund_policy.txt:1]."
    )

    result = extract_citations(answer)

    assert result == [
        "[refund_policy.txt:0]",
        "[refund_policy.txt:1]"
    ]


def test_extract_citations_without_citations():
    answer = "Refunds within 30 days."

    result = extract_citations(answer)

    assert result == []


def test_extract_citations_unknown_chunk():
    answer = "Refunds within 30 days [refund_policy.txt:99]."

    result = extract_citations(answer)

    assert result == ["[refund_policy.txt:99]"]


def test_validate_citations_mixed():
    answer = (
        "Refunds within 30 days [refund_policy.txt:0]. "
        "A receipt is required [refund_policy.txt:99]."
    )

    retrieved_records = [
        {
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "text": "Refunds within 30 days."
        },
        {
            "source": "refund_policy.txt",
            "chunk_id": 1,
            "text": "A valid receipt is required."
        }
    ]

    result = validate_citations(answer, retrieved_records)

    assert result["valid_citations"] == ["[refund_policy.txt:0]"]
    assert result["invalid_citations"] == ["[refund_policy.txt:99]"]


def test_validate_citations_without_citations():
    answer = ("Refunds within 30 days.")

    retrieved_records = [
        {
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "text": "Refunds within 30 days."
        }]

    result = validate_citations(answer, retrieved_records)

    assert result["valid_citations"] == []
    assert result["invalid_citations"] == []


def test_validate_citations_without_evidence():
    answer = ("Refunds within 30 days [refund_policy.txt:0].")

    retrieved_records = []

    result = validate_citations(answer, retrieved_records)

    assert result["valid_citations"] == []
    assert result["invalid_citations"] == ["[refund_policy.txt:0]"]