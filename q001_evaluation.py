
import psycopg

from llm_probe import generate_sql
from q001_policy import extract_q001_date_bounds
from reader_check import execute_q001_bounds
from evaluators import check_integer_answer


EXPECTED_ANSWER = 7


def evaluate_q001_sql(sql):
    bounds = extract_q001_date_bounds(sql)

    if bounds is None:
        return {
            "status": "REJECTED",
            "actual_answer": None,
            "expected_answer": EXPECTED_ANSWER,
        }

    start_date, end_date = bounds

    try:
        actual_answer = execute_q001_bounds(start_date, end_date)
    except (psycopg.Error, RuntimeError) as error:
        return {
            "status": "ERROR",
            "error_type": type(error).__name__,
            "actual_answer": None,
            "expected_answer": EXPECTED_ANSWER,
        }

    passed = check_integer_answer(actual_answer, EXPECTED_ANSWER)

    return {
        "status": "PASS" if passed else "FAIL",
        "actual_answer": actual_answer,
        "expected_answer": EXPECTED_ANSWER,
    }


def run_q001_live():
    sql = generate_sql()

    print("Model-generated SQL:")
    print(sql)

    result = evaluate_q001_sql(sql)

    print("Q001 evaluation result:", result)

    return result


if __name__ == "__main__":
    run_q001_live()
