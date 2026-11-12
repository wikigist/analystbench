from rag.retrieval_eval import recall_at_k
from rag.retrieval_eval import recall_at_k, precision_at_k


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