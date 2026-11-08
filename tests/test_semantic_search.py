from rag.semantic_search import retrieve_by_meaning
from rag.semantic_search import index_records
from rag.semantic_search import search_index
from rag.semantic_search import search_index_top_k


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


def test_index_records_adds_embeddings():
    records = [
        {
            "text": "Customers can request refunds.",
            "source": "refund_policy.txt"
        }
    ]

    result = index_records(records, embed_fn=fake_embed)

    assert result[0]["vector"] == [0.5, 0.5]
    assert result[0]["source"] == "refund_policy.txt"
    assert "vector" not in records[0]



def test_search_index_reuses_document_embeddings():
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

    indexed_records = index_records(records, embed_fn=fake_embed)

    result = search_index(
        "How can I get my money back?",
        indexed_records,
        embed_fn=fake_embed
    )

    assert result["source"] == "refund_policy.txt"
    assert result["vector"] == [0.5, 0.5]



def test_search_index_only_embeds_question():
    calls = []

    def counting_embed(text):
        calls.append(text)
        return fake_embed(text)

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

    indexed_records = index_records(
        records,
        embed_fn=counting_embed
    )

    assert len(calls) == 2

    result = search_index(
        "How can I get my money back?",
        indexed_records,
        embed_fn=counting_embed
    )

    assert len(calls) == 3
    assert calls == [
    "Employees must complete training.",
    "Customers can request refunds.",
    "How can I get my money back?"
    ]
    assert result["source"] == "refund_policy.txt"


def test_search_index_top_k():
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

    indexed_records = index_records(
        records,
        embed_fn=fake_embed
    )

    result = search_index_top_k(
        "How can I get my money back?",
        indexed_records,
        k=2,
        embed_fn=fake_embed
    )

    assert result == [indexed_records[1], indexed_records[0]]