from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

schema = """
Table: contact_events
Columns:
contact_id TEXT
customer_id TEXT
started_at TIMESTAMP
ended_at TIMESTAMP
channel TEXT
contact_reason TEXT
"""

question = "How many customer contacts were recorded in September 2026?"

response = client.responses.create(
    model="gpt-5.4-mini",
    instructions=(
        "Write a PostgreSQL SELECT query using only the provided schema. "
        "Return SQL only, without Markdown or explanation."
    ),
    input=f"Schema:\n{schema}\n\nQuestion:\n{question}",
    max_output_tokens=400,
    store=False,
)

print(response.output_text)