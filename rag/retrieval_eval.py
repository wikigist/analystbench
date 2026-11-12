def recall_at_k(retrieved_ids, relevant_ids, k):
    relevant = set(relevant_ids)

    if not relevant:
        return 0.0

    top_k = set(retrieved_ids[:k])

    matches = top_k.intersection(relevant)

    return len(matches) / len(relevant)


def precision_at_k(retrieved_ids, relevant_ids, k):
    top_k = retrieved_ids[:k]

    if not top_k:
        return 0.0

    relevant = set(relevant_ids)

    matches = sum(
        document_id in relevant
        for document_id in top_k
    )

    return matches / len(top_k)


def chunk_key(record):
    return (record["source"], record["chunk_id"])


def evaluate_retrieved_chunks(retrieved_records, relevant_records, k):
    retrieved_keys = []
    relevant_keys = []

    for record in retrieved_records:
        retrieved_keys.append(chunk_key(record))

    for record in relevant_records:
        relevant_keys.append(chunk_key(record))

    return {
        "recall": recall_at_k(retrieved_keys, relevant_keys, k),
        "precision": precision_at_k(retrieved_keys, relevant_keys, k)
    }