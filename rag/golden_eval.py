from rag.pipeline import index_file
from rag.semantic_search import search_index_top_k
from rag.retrieval_eval import evaluate_retrieved_chunks
import hashlib
from pathlib import Path
from rag.storage import save_index, load_index


def evaluate_golden_cases(cases, embed_fn, k=1, cache_dir=None, embedding_id=None):
    results = []
    index_cache = {}

    if cache_dir is not None:
            if embedding_id is None:
                 raise ValueError("embedding_id is required for persistent caching")

            cache_dir = Path(cache_dir)

    for case in cases:
         file_path = Path(case["file_path"])
         document_hash = hashlib.sha256(
              file_path.read_bytes()
              ).hexdigest()

         cache_key = (
            case["file_path"],
            case["chunk_size"],
            case["overlap"],
            document_hash,
            embedding_id
            )

         cache_file = None
         if cache_dir is not None:
             key_text = repr(cache_key)
             key_hash = hashlib.sha256(key_text.encode("utf-8")).hexdigest()
             cache_file = cache_dir / f"{key_hash}.json"

         if cache_key not in index_cache:
                 if cache_file is not None and cache_file.exists():
                      index_cache[cache_key] = load_index(cache_file)

                 else:
                      index_cache[cache_key] = index_file(
                            file_path=case["file_path"],
                            chunk_size=case["chunk_size"],
                            overlap=case["overlap"],
                            embed_fn=embed_fn
                            )

                      if cache_file is not None:
                           save_index(index_cache[cache_key], cache_file)

         records = index_cache[cache_key]

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