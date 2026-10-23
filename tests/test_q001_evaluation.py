import q001_evaluation
from datetime import date


SEPTEMBER_SQL = (
    "SELECT COUNT(*) FROM contact_events "
    "WHERE started_at >= DATE '2026-09-01' "
    "AND started_at < DATE '2026-10-01';"
)


def test_q001_pass(monkeypatch):
    def fake_database_query(start_date, end_date):
        return 7

    monkeypatch.setattr(
        q001_evaluation,
        "execute_q001_bounds",
        fake_database_query,
    )

    result = q001_evaluation.evaluate_q001_sql(SEPTEMBER_SQL)

    assert result["status"] == "PASS"
    assert result["actual_answer"] == 7


def test_q001_fail(monkeypatch):
    def fake_database_query(start_date, end_date):
        return 3

    monkeypatch.setattr(
        q001_evaluation,
        "execute_q001_bounds",
        fake_database_query,
    )

    result = q001_evaluation.evaluate_q001_sql(SEPTEMBER_SQL)

    assert result["status"] == "FAIL"
    assert result["actual_answer"] == 3


def test_q001_rejected_without_database_execution(monkeypatch):
    def fake_database_query(start_date, end_date):
        raise AssertionError("Database must not be called")

    monkeypatch.setattr(
        q001_evaluation,
        "execute_q001_bounds",
        fake_database_query,
    )

    result = q001_evaluation.evaluate_q001_sql(
        "DELETE FROM contact_events;"
    )

    assert result["status"] == "REJECTED"



def test_q001_database_error(monkeypatch):

    def fake_database_query(start_date, end_date):
        raise q001_evaluation.psycopg.OperationalError(
            "Database unavailable"
        )

    monkeypatch.setattr(
        q001_evaluation,
        "execute_q001_bounds",
        fake_database_query,
    )

    result = q001_evaluation.evaluate_q001_sql(
        SEPTEMBER_SQL
    )

    assert result["status"] == "ERROR"
    assert result["actual_answer"] is None
    assert result["error_type"] == "OperationalError"



def test_q001_missing_password_error(monkeypatch):

    def fake_database_query(start_date, end_date):
        raise RuntimeError("Reader database password is missing")

    monkeypatch.setattr(
        q001_evaluation,
        "execute_q001_bounds",
        fake_database_query,
    )

    result = q001_evaluation.evaluate_q001_sql(
        SEPTEMBER_SQL
    )

    assert result["status"] == "ERROR"
    assert result["actual_answer"] is None
    assert result["error_type"] == "RuntimeError"



def test_q001_august_dates_reach_database(monkeypatch):

    def fake_database_query(start_date, end_date):
        assert start_date == date(2026, 8, 1)
        assert end_date == date(2026, 9, 1)
        return 0

    monkeypatch.setattr(
        q001_evaluation,
        "execute_q001_bounds",
        fake_database_query,
    )

    august_sql = (
        "SELECT COUNT(*) FROM contact_events "
        "WHERE started_at >= DATE '2026-08-01' "
        "AND started_at < DATE '2026-09-01';"
    )

    result = q001_evaluation.evaluate_q001_sql(august_sql)

    assert result["status"] == "FAIL"
    assert result["actual_answer"] == 0
