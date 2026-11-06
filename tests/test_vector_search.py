from rag.vector_search import vector_distance


def test_vector_distance_identical_vectors():
    result = vector_distance([0.5, 0.5], [0.5, 0.5])

    assert result == 0.0

def test_vector_distance_different_vectors():
    result = vector_distance([0, 0], [3, 4])

    assert result == 5.0