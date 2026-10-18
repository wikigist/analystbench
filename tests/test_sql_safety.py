from sql_safety import inspect_sql


def test_rejects_delete_statement():
    result = inspect_sql("DELETE FROM contact_events;")

    assert result is False



def test_accepts_select_statement():
    result = inspect_sql("SELECT COUNT(*) FROM contact_events;")

    assert result is True


def test_rejects_multiple_statements():
    result = inspect_sql(
        "SELECT COUNT(*) FROM contact_events;"
        "DELETE FROM contact_events;")

    assert result is False


def test_rejects_malformed_sql():
    result = inspect_sql("SELECT * FROM (")

    assert result is False


def test_rejects_sleep_function():
    result = inspect_sql("SELECT pg_sleep(10);")

    assert result is False
