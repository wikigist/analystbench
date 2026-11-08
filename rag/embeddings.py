from dotenv import load_dotenv
from openai import OpenAI


def embed_text(text):
    load_dotenv()

    client = OpenAI()

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding