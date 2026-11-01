from result_history import save_result


def report_result(case_id, expected, actual, passed, run_id=None):
    print(case_id)
    print("Expected:", expected)
    print("Actual:", actual)

    if passed:
        print("PASS")
    else:
        print("FAIL")

    save_result(case_id, passed, run_id=run_id)