from datetime import date

from q002_policy import extract_q002_date_bounds


def test_q002_accepts_distinct_customer_count():
    sql = """
    SELECT COUNT(DISTINCT customer_id)
    FROM contact_events
    WHERE started_at >= DATE '2026-09-01'
      AND started_at < DATE '2026-10-01';
    """

    result = extract_q002_date_bounds(sql)

    assert result == (
        date(2026, 9, 1),
        date(2026, 10, 1)
    )


def test_q002_rejects_counting_all_contacts():
    sql = """
    SELECT COUNT(*)
    FROM contact_events
    WHERE started_at >= DATE '2026-09-01'
      AND started_at < DATE '2026-10-01';
    """

    result = extract_q002_date_bounds(sql)

    assert result is None
