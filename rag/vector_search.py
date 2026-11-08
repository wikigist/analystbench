from math import dist


def vector_distance(vector_a, vector_b):
    return dist(vector_a, vector_b)


def find_closest_vector(question_vector, document_vectors):
    best_index = 0

    best_distance = vector_distance(
        question_vector,
        document_vectors[0]
    )

    for index, vector in enumerate(document_vectors):
        distance = vector_distance(question_vector, vector)

        if distance < best_distance:
            best_distance = distance
            best_index = index

    return best_index


def find_closest_record(question_vector, records):
    document_vectors = []

    for record in records:
        document_vectors.append(record["vector"])

    closest_index = find_closest_vector(
        question_vector,
        document_vectors
    )

    return records[closest_index]


def find_top_k_records(question_vector, records, k=2):
    ranked_records = sorted(
        records,
        key=lambda record: vector_distance(
            question_vector,
            record["vector"]
        )
    )

    return ranked_records[:k]