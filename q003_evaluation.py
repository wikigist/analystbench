import json
import psycopg

from evaluators import check_ranked_answer
from q003_reader import execute_q003_bounds
from q003_policy import extract_q003_date_bounds
from datetime import date
from llm_probe import generate_sql


Q003_SCHEMA = """
Table: agent_interactions
Columns:
queue_id TEXT
started_at TIMESTAMP

Table: queues
Columns:
queue_id TEXT
queue_name TEXT
"""


def get_q003_expected_answer():
    with open("benchmarks/benchmark_cases.json") as file:
        cases = json.load(file)

    for case in cases:
        if case["id"] == "Q003":
            return case["expected_answer"]

    raise ValueError("Q003 benchmark not found")


def evaluate_q003_bounds(start_date, end_date):
    expected_answer = get_q003_expected_answer()

    try:
        actual_answer = execute_q003_bounds(start_date, end_date)
    except (psycopg.Error, RuntimeError) as error:
        return {
            "status": "ERROR",
            "actual_answer": None,
            "expected_answer": expected_answer,
            "error_type": type(error).__name__,
        }

    passed = check_ranked_answer(actual_answer, expected_answer)

    return {
        "status": "PASS" if passed else "FAIL",
        "actual_answer": actual_answer,
        "expected_answer": expected_answer,
    }



def evaluate_q003_sql(sql):
    bounds = extract_q003_date_bounds(sql)

    if bounds is None:
        return {
            "status": "REJECTED",
            "actual_answer": None,
            "expected_answer": get_q003_expected_answer(),
        }

    start_date, end_date = bounds

    result = evaluate_q003_bounds(start_date, end_date)

    if result["status"] == "ERROR":
        return result

    dates_correct = (
        start_date == date(2026, 9, 1)
        and end_date == date(2026, 10, 1)
    )

    result["date_filter_correct"] = dates_correct

    if not dates_correct:
        result["status"] = "FAIL"
        result["failure_reason"] = "Wrong date range for Q003"

    return result



def run_q003_live():
    question = (
    "Rank all queues by the number of agent interactions "
    "in September 2026, highest to lowest. "
    "Return every queue's name and interaction count."
)

    sql = generate_sql(
        question_text=question,
        schema_text=Q003_SCHEMA,
    )

    print("Model-generated Q003 SQL:")
    print(sql)

    result = evaluate_q003_sql(sql)

    print("Q003 evaluation result:", result)

    return result


if __name__ == "__main__":
    run_q003_live()