from rag.pipeline import index_file
from rag.semantic_search import search_index_top_k
from rag.retrieval_eval import evaluate_retrieved_chunks


def evaluate_golden_cases(cases, embed_fn, k=1):
    results = []

    for case in cases:
        records = index_file(
            file_path=case["file_path"],
            chunk_size=case["chunk_size"],
            overlap=case["overlap"],
            embed_fn=embed_fn
        )

        retrieved = search_index_top_k(
            case["question"],
            records,
            k=k,
            embed_fn=embed_fn
        )

        metrics = evaluate_retrieved_chunks(
            retrieved,
            case["relevant_records"],
            k=k
        )

        results.append({
            "case_id": case["case_id"],
            "retrieved_chunk_ids": [
                record["chunk_id"] for record in retrieved
                ],
            "recall": metrics["recall"],
            "precision": metrics["precision"]
        })

    return results