from datetime import date

import q003_evaluation


SEPTEMBER_START = date(2026, 9, 1)
SEPTEMBER_END = date(2026, 10, 1)

CORRECT_RANKING = [
    {"queue_name": "General Enquiries", "interaction_count": 5},
    {"queue_name": "Payments", "interaction_count": 3},
    {"queue_name": "Complaints", "interaction_count": 2},
]


def test_q003_pass(monkeypatch):
    def fake_database_query(start_date, end_date):
        assert start_date == SEPTEMBER_START
        assert end_date == SEPTEMBER_END
        return CORRECT_RANKING

    monkeypatch.setattr(
        q003_evaluation,
        "execute_q003_bounds",
        fake_database_query,
    )

    result = q003_evaluation.evaluate_q003_bounds(
        SEPTEMBER_START,
        SEPTEMBER_END,
    )

    assert result["status"] == "PASS"
    assert result["actual_answer"] == CORRECT_RANKING


def test_q003_wrong_ranking_fails(monkeypatch):
    def fake_database_query(start_date, end_date):
        return [
            CORRECT_RANKING[1],
            CORRECT_RANKING[0],
            CORRECT_RANKING[2],
        ]

    monkeypatch.setattr(
        q003_evaluation,
        "execute_q003_bounds",
        fake_database_query,
    )

    result = q003_evaluation.evaluate_q003_bounds(
        SEPTEMBER_START,
        SEPTEMBER_END,
    )

    assert result["status"] == "FAIL"


def test_q003_database_error(monkeypatch):
    def fake_database_query(start_date, end_date):
        raise RuntimeError("Database unavailable")

    monkeypatch.setattr(
        q003_evaluation,
        "execute_q003_bounds",
        fake_database_query,
    )

    result = q003_evaluation.evaluate_q003_bounds(
        SEPTEMBER_START,
        SEPTEMBER_END,
    )

    assert result["status"] == "ERROR"
    assert result["actual_answer"] is None
    assert result["error_type"] == "RuntimeError"



def test_q003_wrong_month_fails_even_if_answer_matches(monkeypatch):
    def fake_database_query(start_date, end_date):
        assert start_date == date(2026, 8, 1)
        assert end_date == date(2026, 9, 1)
        return CORRECT_RANKING

    monkeypatch.setattr(
        q003_evaluation,
        "execute_q003_bounds",
        fake_database_query,
    )

    august_sql = """
    SELECT q.queue_name, COUNT(*) AS interaction_count
    FROM agent_interactions ai
    JOIN queues q ON ai.queue_id = q.queue_id
    WHERE ai.started_at >= DATE '2026-08-01'
      AND ai.started_at < DATE '2026-09-01'
    GROUP BY q.queue_name
    ORDER BY interaction_count DESC;
    """

    result = q003_evaluation.evaluate_q003_sql(august_sql)

    assert result["actual_answer"] == CORRECT_RANKING
    assert result["date_filter_correct"] is False
    assert result["status"] == "FAIL"