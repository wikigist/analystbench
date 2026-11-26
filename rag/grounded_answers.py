def build_grounded_prompt(question, retrieved_records):
    evidence_lines = []

    for record in retrieved_records:
        evidence_lines.append(
            f"[{record['source']}:{record['chunk_id']}] {record['text']}"
        )

    evidence = "\n".join(evidence_lines)

    prompt = (
        "Answer the question using only the evidence below.\n"
        "If the evidence is insufficient, say you don't know.\n"
        "Cite the evidence labels you use.\n\n"
        f"Evidence:\n{evidence}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )

    return prompt


def generate_grounded_answer(question, retrieved_records, generate_fn):

    if not retrieved_records:
        return "I don't know."

    prompt = build_grounded_prompt(question, retrieved_records)

    return generate_fn(prompt)