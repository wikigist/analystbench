from datetime import date

import q002_evaluation


SEPTEMBER_SQL = """
SELECT COUNT(DISTINCT customer_id)
FROM contact_events
WHERE started_at >= DATE '2026-09-01'
AND started_at < DATE '2026-10-01';
"""


def test_q002_pass(monkeypatch):
    def fake_database_query(start_date, end_date):
        assert start_date == date(2026, 9, 1)
        assert end_date == date(2026, 10, 1)
        return 4

    monkeypatch.setattr(
        q002_evaluation,
        "execute_q002_bounds",
        fake_database_query,
    )

    result = q002_evaluation.evaluate_q002_sql(SEPTEMBER_SQL)

    assert result["status"] == "PASS"
    assert result["actual_answer"] == 4


def test_q002_fail(monkeypatch):
    def fake_database_query(start_date, end_date):
        return 2

    monkeypatch.setattr(
        q002_evaluation,
        "execute_q002_bounds",
        fake_database_query,
    )

    result = q002_evaluation.evaluate_q002_sql(SEPTEMBER_SQL)

    assert result["status"] == "FAIL"
    assert result["actual_answer"] == 2


def test_q002_rejects_count_all(monkeypatch):
    def fake_database_query(start_date, end_date):
        raise AssertionError("Database must not be called")

    monkeypatch.setattr(
        q002_evaluation,
        "execute_q002_bounds",
        fake_database_query,
    )

    wrong_sql = SEPTEMBER_SQL.replace(
        "COUNT(DISTINCT customer_id)",
        "COUNT(*)",
    )

    result = q002_evaluation.evaluate_q002_sql(wrong_sql)

    assert result["status"] == "REJECTED"


def test_q002_database_error(monkeypatch):
    def fake_database_query(start_date, end_date):
        raise RuntimeError("Database configuration error")

    monkeypatch.setattr(
        q002_evaluation,
        "execute_q002_bounds",
        fake_database_query,
    )

    result = q002_evaluation.evaluate_q002_sql(SEPTEMBER_SQL)

    assert result["status"] == "ERROR"
    assert result["error_type"] == "RuntimeError"