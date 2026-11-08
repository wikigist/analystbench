from rag.embeddings import embed_text
from rag.vector_search import find_closest_record
from rag.vector_search import find_top_k_records


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



def index_records(records, embed_fn=embed_text):
    indexed_records = []

    for record in records:
        indexed_record = record.copy()

        indexed_record["vector"] = embed_fn(record["text"])

        indexed_records.append(indexed_record)

    return indexed_records


def search_index(question, indexed_records, embed_fn=embed_text):
    if not indexed_records:
        return None

    question_vector = embed_fn(question)

    return find_closest_record(
        question_vector,
        indexed_records
    )


def search_index_top_k(
    question,
    indexed_records,
    k=2,
    embed_fn=embed_text
):
    if not indexed_records:
        return []

    question_vector = embed_fn(question)

    return find_top_k_records(
        question_vector,
        indexed_records,
        k=k
    )