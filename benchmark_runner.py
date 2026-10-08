import json 
import psycopg

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

                print(case["id"])
                print("Expected:", expected_answer)
                print("Actual:", actual_answer)

                if actual_answer == expected_answer:
                    print("PASS")
                else:
                    print("FAIL")

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
                    
                    print(case["id"])
                    print("Expected:", expected_answer)
                    print("Actual:", actual_answer)

                    if actual_answer == expected_answer:
                         print("PASS")

                    else:
                         print("FAIL")