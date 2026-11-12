from rag.retrieval_eval import recall_at_k
from rag.retrieval_eval import recall_at_k, precision_at_k
from rag.retrieval_eval import recall_at_k, precision_at_k, chunk_key
from rag.retrieval_eval import evaluate_retrieved_chunks


def test_recall_at_3():
    retrieved_ids = [2, 7, 9]

    relevant_ids = [2, 7, 11, 15]

    result = recall_at_k(
        retrieved_ids,
        relevant_ids,
        k=3
    )

    assert result == 0.5


def test_recall_at_1():
    retrieved_ids = [2, 7, 9]

    relevant_ids = [2, 7, 11, 15]

    result = recall_at_k(
        retrieved_ids,
        relevant_ids,
        k=1
    )

    assert result == 0.25


def test_recall_at_3_with_irrelevant_first_result():
    retrieved_ids = [9, 2, 7]
    relevant_ids = [2, 7, 11, 15]

    result = recall_at_k(
        retrieved_ids,
        relevant_ids,
        k=3
    )

    assert result == 0.5


def test_precision_at_3():
    retrieved_ids = [9, 2, 7]
    relevant_ids = [2, 7, 11, 15]

    result = precision_at_k(
        retrieved_ids,
        relevant_ids,
        k=3
    )

    assert result == 2 / 3


def test_empty_retrieval():
    retrieved_ids = []
    relevant_ids = [2, 7]

    recall = recall_at_k(
        retrieved_ids,
        relevant_ids,
        k=3
    )

    precision = precision_at_k(
        retrieved_ids,
        relevant_ids,
        k=3
    )

    assert recall == 0.0
    assert precision == 0.0


def test_chunk_key_distinguishes_documents():
    refund = {
        "source": "refund_policy.txt",
        "chunk_id": 2
    }

    training = {
        "source": "training_policy.txt",
        "chunk_id": 2
    }

    refund_key = chunk_key(refund)
    training_key = chunk_key(training)

    assert refund_key == ("refund_policy.txt", 2)
    assert training_key == ("training_policy.txt", 2)

    assert refund_key != training_key



def test_evaluate_retrieved_chunks():
    retrieved_records = [
        {"source": "training_policy.txt", "chunk_id": 2},
        {"source": "refund_policy.txt", "chunk_id": 2}
    ]

    relevant_records = [
        {"source": "refund_policy.txt", "chunk_id": 2},
        {"source": "refund_policy.txt", "chunk_id": 3}
    ]

    result = evaluate_retrieved_chunks(
        retrieved_records,
        relevant_records,
        k=2
    )

    assert result["recall"] == 0.5
    assert result["precision"] == 0.5