import os
import psycopg
from dotenv import load_dotenv
from evaluators import check_integer_answer

load_dotenv()

password_loaded = bool(os.getenv("ANALYSTBENCH_READER_PASSWORD"))

print("Reader password loaded:", password_loaded)


with psycopg.connect(
    dbname="analystbench",
    user="analystbench_reader",
    host="localhost",
    password=os.getenv("ANALYSTBENCH_READER_PASSWORD"),
    connect_timeout=5
) as connection:

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_user;")

        result = cursor.fetchone()

        print("Connected as:", result[0])

        if result[0] != "analystbench_reader":
            raise RuntimeError("Unsafe database account detected")

        # print("Cursor closed before Q001:", cursor.closed)

        cursor.execute("""
        SELECT COUNT(*) AS customer_contacts
        FROM contact_events
        WHERE started_at >= TIMESTAMP '2026-09-01'
        AND started_at < TIMESTAMP '2026-10-01';""")
        
        model_result = cursor.fetchone()[0]
        print("LLM SQL result:", model_result)

        expected_answer = 7

        passed = check_integer_answer(model_result, expected_answer)

        print("Q001 evaluation passed:", passed)