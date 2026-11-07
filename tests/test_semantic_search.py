from rag.semantic_search import retrieve_by_meaning


def fake_embed(text):
    vectors = {
        "How can I get my money back?": [0.5, 0.5],
        "Employees must complete training.": [0.1, 0.9],
        "Customers can request refunds.": [0.5, 0.5]
    }

    return vectors[text]


def test_retrieve_by_meaning():
    records = [
        {
            "text": "Employees must complete training.",
            "source": "training_policy.txt"
        },
        {
            "text": "Customers can request refunds.",
            "source": "refund_policy.txt"
        }
    ]

    result = retrieve_by_meaning(
        "How can I get my money back?",
        records,
        embed_fn=fake_embed
    )

    assert result["source"] == "refund_policy.txt"
    assert result["vector"] == [0.5, 0.5]
    assert "vector" not in records[1]


def test_retrieve_by_meaning_empty_records():
    result = retrieve_by_meaning(
        "How can I get my money back?",
        [],
        embed_fn=fake_embed
    )

    assert result is None