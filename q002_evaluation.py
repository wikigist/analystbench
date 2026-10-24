from count_evaluation import evaluate_count_sql
from q002_policy import extract_q002_date_bounds
from reader_check import execute_q002_bounds
from llm_probe import generate_sql


EXPECTED_ANSWER = 4


def evaluate_q002_sql(sql):
    return evaluate_count_sql(
        sql,
        extract_q002_date_bounds,
        execute_q002_bounds,
        EXPECTED_ANSWER,
    )

def run_q002_live():
    question = "How many customers contacted us in September 2026?"

    sql = generate_sql(question)

    print("Model-generated Q002 SQL:")
    print(sql)

    result = evaluate_q002_sql(sql)

    print("Q002 evaluation result:", result)

    return result


if __name__ == "__main__":
    run_q002_live()