from datetime import date

from q001_policy import extract_q001_date_bounds


def test_accepts_q001_dates():
    sql = """
        SELECT COUNT(*) AS contact_count
        FROM contact_events
        WHERE started_at >= DATE '2026-09-01'
          AND started_at < DATE '2026-10-01';
    """

    result = extract_q001_date_bounds(sql)

    assert result == (date(2026, 9, 1), date(2026, 10, 1))


def test_rejects_wrong_table():
    sql = "SELECT COUNT(*) FROM payments;"

    result = extract_q001_date_bounds(sql)

    assert result is None


def test_accepts_different_dates_for_evaluation():
    sql = """
        SELECT COUNT(*) FROM contact_events
        WHERE started_at >= DATE '2026-08-01'
          AND started_at < DATE '2026-09-01';
    """

    result = extract_q001_date_bounds(sql)

    assert result == (date(2026, 8, 1), date(2026, 9, 1))
