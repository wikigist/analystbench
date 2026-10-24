import psycopg

from evaluators import check_integer_answer


def evaluate_count_sql(
    sql,
    date_extractor,
    database_counter,
    expected_answer,
):
    bounds = date_extractor(sql)

    if bounds is None:
        return {
            "status": "REJECTED",
            "actual_answer": None,
            "expected_answer": expected_answer,
        }

    start_date, end_date = bounds

    try:
        actual_answer = database_counter(start_date, end_date)
    except (psycopg.Error, RuntimeError) as error:
        return {
            "status": "ERROR",
            "error_type": type(error).__name__,
            "actual_answer": None,
            "expected_answer": expected_answer,
        }

    passed = check_integer_answer(
        actual_answer,
        expected_answer,
    )

    return {
        "status": "PASS" if passed else "FAIL",
        "actual_answer": actual_answer,
        "expected_answer": expected_answer,
    }
