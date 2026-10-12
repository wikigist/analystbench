def check_integer_answer(actual, expected):
    return actual == expected


def check_ranked_answer(actual, expected):
    return  actual == expected


def check_unordered_answer(actual, expected, key_field="customer_id"):
    actual_sorted = sorted(actual, key=lambda row: row[key_field])
    expected_sorted = sorted(expected, key=lambda row: row[key_field])

    return actual_sorted == expected_sorted

