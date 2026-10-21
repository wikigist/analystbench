
import re
from datetime import date

from sql_safety import inspect_sql


Q001_PATTERN = re.compile(
    r"""
    SELECT\s+COUNT\s*\(\s*\*\s*\)
    (?:\s+AS\s+[A-Za-z_][A-Za-z_0-9]*)?
    \s+FROM\s+(?:public\.)?contact_events
    \s+WHERE\s+started_at\s*>=\s*(?:DATE|TIMESTAMP)\s*'(?P<start>\d{4}-\d{2}-\d{2})'
    \s+AND\s+started_at\s*<\s*(?:DATE|TIMESTAMP)\s*'(?P<end>\d{4}-\d{2}-\d{2})'
    \s*;?\s*
    """,
    re.IGNORECASE | re.VERBOSE,
)


def extract_q001_date_bounds(sql):
    if inspect_sql(sql) is not True:
        return None

    match = Q001_PATTERN.fullmatch(sql.strip())

    if match is None:
        return None

    try:
        start_date = date.fromisoformat(match.group("start"))
        end_date = date.fromisoformat(match.group("end"))
    except ValueError:
        return None

    return start_date, end_date
