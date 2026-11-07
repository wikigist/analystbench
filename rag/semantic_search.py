from rag.embeddings import embed_text
from rag.vector_search import find_closest_record


def retrieve_by_meaning(question, records, embed_fn=embed_text):
    if not records:
        return None

    question_vector = embed_fn(question)

    vector_records = []

    for record in records:
        vector_record = record.copy()

        vector_record["vector"] = embed_fn(record["text"])

        vector_records.append(vector_record)

    return find_closest_record(question_vector, vector_records)