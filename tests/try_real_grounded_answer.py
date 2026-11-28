from rag.semantic_search import index_records
from rag.pipeline import answer_from_index
from rag.generation import generate_text


if __name__ == "__main__":

    question = "What is the refund period and do I need a receipt?"

    records = [
        {
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "text": "Refunds within 30 days."
        },
        {
            "source": "refund_policy.txt",
            "chunk_id": 1,
            "text": "A valid receipt is required."
        }
    ]

    indexed_records = index_records(records)

    answer = answer_from_index(
        question,
        indexed_records,
        generate_text,
        k=2
    )

    print("Generated answer:")
    print(answer)

    unsupported_question = "How much does international delivery cost?"

    unsupported_answer = answer_from_index(
        unsupported_question,
        indexed_records,
        generate_text,
        k=2
    )

    print("\nUnsupported question:")
    print(unsupported_question)

    print("Generated answer:")
    print(unsupported_answer)