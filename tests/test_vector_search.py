from rag.vector_search import vector_distance
from rag.vector_search import find_closest_vector
from rag.vector_search import find_closest_record
from rag.vector_search import find_top_k_records


def test_vector_distance_identical_vectors():
    result = vector_distance([0.5, 0.5], [0.5, 0.5])

    assert result == 0.0

def test_vector_distance_different_vectors():
    result = vector_distance([0, 0], [3, 4])

    assert result == 5.0

def test_find_closest_vector():
    question = [0.5, 0.5]

    documents = [
        [0.1, 0.9],
        [0.5, 0.5],
        [0.8, 0.2]
    ]

    result = find_closest_vector(question, documents)

    assert result == 1


def test_find_closest_vector_last_position():
    question = [0.5, 0.5]

    documents = [
        [0.1, 0.9],
        [0.8, 0.2],
        [0.5, 0.5]
    ]

    result = find_closest_vector(question, documents)

    assert result == 2


def test_find_closest_record():
    question = [0.5, 0.5]

    records = [
        {
            "text": "Employees must complete training.",
            "source": "training_policy.txt",
            "vector": [0.1, 0.9]
        },
        {
            "text": "Customers can request refunds.",
            "source": "refund_policy.txt",
            "vector": [0.5, 0.5]
        }
    ]

    result = find_closest_record(question, records)

    assert result == records[1]


def test_find_top_k_records():
    question = [0.0, 0.0]

    records = [
        {
            "text": "Refund policy",
            "vector": [0.2, 0.0]
        },
        {
            "text": "Training policy",
            "vector": [0.9, 0.0]
        },
        {
            "text": "Refund approval policy",
            "vector": [0.3, 0.0]
        }
    ]

    result = find_top_k_records(question, records, k=2)

    assert result == [records[0], records[2]]