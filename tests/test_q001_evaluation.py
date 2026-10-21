
import q001_evaluation


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
