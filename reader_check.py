
import os
import psycopg
from dotenv import load_dotenv
from evaluators import check_integer_answer
from datetime import date


def execute_q001_bounds(start_date, end_date):
    load_dotenv()

    password = os.getenv("ANALYSTBENCH_READER_PASSWORD")

    if not password:
        raise RuntimeError("Reader database password is missing")

    with psycopg.connect(
        dbname="analystbench",
        user="analystbench_reader",
        host="localhost",
        password=password,
        connect_timeout=5,
    ) as connection:

        with connection.cursor() as cursor:

            # Make this transaction read-only
            cursor.execute("SET TRANSACTION READ ONLY;")

            # Verify the database account
            cursor.execute("SELECT current_user;")
            connected_user = cursor.fetchone()[0]

            if connected_user != "analystbench_reader":
                raise RuntimeError("Unsafe database account detected")

            # Execute our fixed, trusted Q001 query
            cursor.execute("""
            SELECT COUNT(*) AS customer_contacts
            FROM public.contact_events
            WHERE started_at >= %s
            AND started_at < %s;
            """, (start_date, end_date))

            actual_answer = cursor.fetchone()[0]

            return actual_answer


def execute_trusted_q001():
    return execute_q001_bounds(
        date(2026, 9, 1),
        date(2026, 10, 1)
    )


if __name__ == "__main__":
    actual_answer = execute_trusted_q001()

    expected_answer = 7

    passed = check_integer_answer(actual_answer, expected_answer)

    print("Trusted Q001 result:", actual_answer)
    print("Q001 evaluation passed:", passed)