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



def test_unordered_answer_passes_for_payment_groups():
    expected = [
        {
            "payment_group": "failed_payment",
            "customer_count": 2,
            "total_contacts": 5,
            "average_contacts": 2.5
        },
        {
            "payment_group": "no_failed_payment",
            "customer_count": 2,
            "total_contacts": 2,
            "average_contacts": 1.0
        }
    ]

    actual = [
        {
            "payment_group": "no_failed_payment",
            "customer_count": 2,
            "total_contacts": 2,
            "average_contacts": 1.0
        },
        {
            "payment_group": "failed_payment",
            "customer_count": 2,
            "total_contacts": 5,
            "average_contacts": 2.5
        }
    ]

    assert check_unordered_answer(actual, expected, "payment_group") is True



def test_unordered_answer_fails_when_average_is_wrong():
    expected = [
        {
            "payment_group": "failed_payment",
            "customer_count": 2,
            "total_contacts": 5,
            "average_contacts": 2.5
        }
    ]

    actual = [
        {
            "payment_group": "failed_payment",
            "customer_count": 2,
            "total_contacts": 5,
            "average_contacts": 3.5
        }
    ]

    assert check_unordered_answer(actual, expected, "payment_group") is False