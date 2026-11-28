from dotenv import load_dotenv
from openai import OpenAI


def generate_text(prompt, model="gpt-5.4-mini"):
    load_dotenv()

    client = OpenAI()

    response = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=400,
        store=False
    )

    return response.output_text.strip()