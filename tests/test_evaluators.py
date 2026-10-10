from evaluators import check_unordered_answer
from evaluators import check_unordered_answer, check_ranked_answer, check_integer_answer


def test_unordered_answer_passes_when_order_changes():
    expected = [
        {"customer_id": "C001", "failed_payment_count": 1},
        {"customer_id": "C003", "failed_payment_count": 1}
    ]

    actual = [
        {"customer_id": "C003", "failed_payment_count": 1},
        {"customer_id": "C001", "failed_payment_count": 1}
    ]

    assert check_unordered_answer(actual, expected) is True


def test_unordered_answer_fails_when_count_is_wrong():
    expected = [
        {"customer_id": "C003", "failed_payment_count": 1}
    ]

    actual = [
        {"customer_id": "C003", "failed_payment_count": 5}
    ]

    assert check_unordered_answer(actual, expected) is False


def test_ranked_answer_fails_when_order_changes():
    expected = [
        {"queue_name": "General Enquiries", "interaction_count": 5},
        {"queue_name": "Payments", "interaction_count": 3}
    ]

    actual = [
        {"queue_name": "Payments", "interaction_count": 3},
        {"queue_name": "General Enquiries", "interaction_count": 5}
    ]

    assert check_ranked_answer(actual, expected) is False



def test_integer_answer_passes_when_counts_match():
    assert check_integer_answer(7, 7) is True


def test_integer_answer_fails_when_counts_differ():
    assert check_integer_answer(8, 7) is False



def test_ranked_answer_passes_when_order_matches():
    expected = [
        {"queue_name": "General Enquiries", "interaction_count": 5},
        {"queue_name": "Payments", "interaction_count": 3}
    ]

    actual = [
        {"queue_name": "General Enquiries", "interaction_count": 5},
        {"queue_name": "Payments", "interaction_count": 3}
    ]

    assert check_ranked_answer(actual, expected) is True