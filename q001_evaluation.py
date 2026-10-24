from count_evaluation import evaluate_count_sql
from llm_probe import generate_sql
from q001_policy import extract_q001_date_bounds
from reader_check import execute_q001_bounds

EXPECTED_ANSWER = 7

def evaluate_q001_sql(sql):
    return evaluate_count_sql(
        sql,
        extract_q001_date_bounds,
        execute_q001_bounds,
        EXPECTED_ANSWER,
    )

def run_q001_live():
    sql = generate_sql()

    print("Model-generated SQL:")
    print(sql)

    result = evaluate_q001_sql(sql)

    print("Q001 evaluation result:", result)

    return result

if __name__ == "__main__":
    run_q001_live()