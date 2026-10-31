import json 
import psycopg
from evaluators import check_integer_answer, check_ranked_answer, check_unordered_answer
from result_history import save_result
from uuid import uuid4

RUN_ID = str(uuid4())

def report_result(case_id, expected, actual, passed):
    print(case_id)
    print("Expected:", expected)
    print("Actual:", actual)
    
    if passed:
        print("PASS")
    else:
        print("FAIL")

    save_result(case_id, passed, run_id=RUN_ID)



with open("benchmarks/benchmark_cases.json", "r") as file:
    benchmark_cases = json.load(file)

with psycopg.connect("dbname=analystbench") as connection:
    with connection.cursor() as cursor:

        for case in benchmark_cases:
            if case["answer_type"] == "integer":
                reference_sql = case["reference_sql"]
                expected_answer = case["expected_answer"]

                cursor.execute(reference_sql)
                result = cursor.fetchone()
                actual_answer = result[0]

                passed = check_integer_answer(actual_answer, expected_answer)

                report_result(case["id"], expected_answer, actual_answer, passed)

            elif case["answer_type"] == "ranked_list":
                    reference_sql = case["reference_sql"]
                    expected_answer = case["expected_answer"]
                    
                    cursor.execute(reference_sql)
                    result = cursor.fetchall()

                    actual_answer = []

                    for row in result:
                         actual_answer.append(
                              {
                                   "queue_name": row[0],
                                   "interaction_count": row[1]
                              }
                         )
                
                    passed = check_ranked_answer(actual_answer, expected_answer)

                    report_result(case["id"], expected_answer, actual_answer, passed)

            elif case["answer_type"] == "unordered_list":
                 reference_sql = case["reference_sql"]
                 expected_answer = case["expected_answer"]

                 cursor.execute(reference_sql)
                 result = cursor.fetchall()

                 column_names = []

                 for column in cursor.description:
                     column_names.append(column.name)

                 actual_answer = []

                 for row in result:
                     actual_answer.append(dict(zip(column_names, row)))


                 sort_key = case.get("sort_key", "customer_id") 
                 passed = check_unordered_answer(actual_answer, expected_answer, sort_key)

                 report_result(case["id"], expected_answer, actual_answer, passed)

           