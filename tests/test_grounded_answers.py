from rag.grounded_answers import build_grounded_prompt, generate_grounded_answer


def test_grounded_prompt_includes_evidence_and_question():
    question = "How long do customers have to request a refund?"

    retrieved_records = [
        {
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "text": "Refunds within 30 days."
        }
    ]

    prompt = build_grounded_prompt(question, retrieved_records)
    assert "[refund_policy.txt:0] Refunds within 30 days." in prompt
    assert "Question: How long do customers have to request a refund?" in prompt


def test_generate_grounded_answer_uses_generator():
    question = "How long is the refund period?"

    retrieved_records = [
        {
            "source": "refund_policy.txt",
            "chunk_id": 0,
            "text": "Refunds within 30 days."
        }
    ]

    received_prompts = []

    def fake_generate(prompt):
        received_prompts.append(prompt)
        return "Customers have 30 days to request a refund."

    answer = generate_grounded_answer(
        question,
        retrieved_records,
        fake_generate
    )

    assert answer == "Customers have 30 days to request a refund."
    assert len(received_prompts) == 1

    assert "[refund_policy.txt:0] Refunds within 30 days." in received_prompts[0]
    assert f"Question: {question}" in received_prompts[0]


def test_generate_grounded_answer_abstains_without_evidence():

    question = "How long is the refund period?"

    retrieved_records = []

    received_prompts = []

    def fake_generate(prompt):
        received_prompts.append(prompt)
        return "Customers have 90 days to request a refund."

    answer = generate_grounded_answer(question, retrieved_records, fake_generate)

    assert answer == "I don't know."
    assert received_prompts == []


def test_grounded_prompt_includes_multiple_evidence_chunks():

    question = "What is the refund period and do I need a receipt?"

    retrieved_records = [
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

    prompt = build_grounded_prompt(question, retrieved_records)

    assert "[refund_policy.txt:0] Refunds within 30 days." in prompt
    assert "[refund_policy.txt:1] A valid receipt is required." in prompt
    assert "Question: What is the refund period and do I need a receipt?" in prompt