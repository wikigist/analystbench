from llm_probe import generate_sql
from sql_safety import inspect_sql


def run_pipeline_probe():
    sql = generate_sql()

    print("Model-generated SQL:")
    print(sql)

    passes_checks = inspect_sql(sql)

    if passes_checks is not True:
        print("SQL rejected. Pipeline stopped.")
        return False

    print("Passed prototype SQL checks:", passes_checks)

    return True


if __name__ == "__main__":
    run_pipeline_probe()
