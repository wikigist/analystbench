def check_integer_answer(actual, expected):
    return actual == expected


def check_ranked_answer(actual, expected):
    return  actual == expected


def check_unordered_answer(actual, expected):
    actual_sorted = sorted(actual, key=lambda row: row["customer_id"])
    expected_sorted = sorted(expected, key=lambda row: row["customer_id"])

    return actual_sorted == expected_sorted

