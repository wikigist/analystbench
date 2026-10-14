from decimal import Decimal

def normalize_row(row):
    normalized = {}

    for key, value in row.items():
        if isinstance(value, float):
            normalized[key] = Decimal(str(value))
        else:
            normalized[key] = value

    return normalized


def check_integer_answer(actual, expected):
    return actual == expected


def check_ranked_answer(actual, expected):
    return  actual == expected


def check_unordered_answer(actual, expected, key_field="customer_id"):
    actual_normalized = []

    for row in actual:
        actual_normalized.append(normalize_row(row))

    expected_normalized = []

    for row in expected:
        expected_normalized.append(normalize_row(row))

    actual_sorted = sorted(actual_normalized, key=lambda row: row[key_field])
    expected_sorted = sorted(expected_normalized, key=lambda row: row[key_field])

    return actual_sorted == expected_sorted


