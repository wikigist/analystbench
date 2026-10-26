import os

import psycopg
from dotenv import load_dotenv


def execute_q003_bounds(start_date, end_date):
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
            cursor.execute("SET TRANSACTION READ ONLY;")

            cursor.execute("SELECT current_user;")
            connected_user = cursor.fetchone()[0]

            if connected_user != "analystbench_reader":
                raise RuntimeError("Unsafe database account detected")

            cursor.execute("""
                SELECT q.queue_name,
                       COUNT(*) AS interaction_count
                FROM public.agent_interactions ai
                JOIN public.queues q
                    ON ai.queue_id = q.queue_id
                WHERE ai.started_at >= %s
                  AND ai.started_at < %s
                GROUP BY q.queue_name
                ORDER BY interaction_count DESC, q.queue_name ASC;
            """, (start_date, end_date))

            rows = cursor.fetchall()

            actual_answer = []

            for row in rows:
                actual_answer.append({
                    "queue_name": row[0],
                    "interaction_count": row[1],
                })

            return actual_answer