import json
from datetime import date

from q003_policy import extract_q003_date_bounds


def get_reference_sql():
    with open("benchmarks/benchmark_cases.json") as file:
        cases = json.load(file)

    for case in cases:
        if case["id"] == "Q003":
            return case["reference_sql"]


def test_q003_accepts_reference_sql():
    sql = get_reference_sql()

    result = extract_q003_date_bounds(sql)

    assert result == (
        date(2026, 9, 1),
        date(2026, 10, 1),
    )


def test_q003_rejects_delete():
    sql = "DELETE FROM agent_interactions;"

    result = extract_q003_date_bounds(sql)

    assert result is None


def test_q003_rejects_wrong_ranking_order():
    sql = get_reference_sql().replace(
        "ORDER BY interaction_count DESC",
        "ORDER BY interaction_count ASC",
    )

    result = extract_q003_date_bounds(sql)

    assert result is None


def test_q003_rejects_wrong_count():
    sql = get_reference_sql().replace(
        "COUNT(ai.queue_id)",
        "COUNT(*)",
    )

    result = extract_q003_date_bounds(sql)

    assert result is None