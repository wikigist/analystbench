import re
from datetime import date

from sql_safety import inspect_sql
import sqlglot
from sqlglot import exp


Q003_PATTERN = re.compile(
    r"""
    SELECT\s+q\.queue_name\s*,\s*COUNT\s*\(\s*ai\.queue_id\s*\)
    \s+AS\s+interaction_count
    \s+FROM\s+(?:public\.)?queues\s+(?:AS\s+)?q
    \s+LEFT\s+JOIN\s+(?:public\.)?agent_interactions\s+(?:AS\s+)?ai
    \s+ON\s+(?:ai\.queue_id\s*=\s*q\.queue_id|q\.queue_id\s*=\s*ai\.queue_id)
    \s+AND\s+ai\.started_at\s*>=\s*
    (?:(?:DATE|TIMESTAMP)\s*)?'(?P<start>\d{4}-\d{2}-\d{2})'
    \s+AND\s+ai\.started_at\s*<\s*
    (?:(?:DATE|TIMESTAMP)\s*)?'(?P<end>\d{4}-\d{2}-\d{2})'
    \s+GROUP\s+BY\s+q\.queue_id\s*,\s*q\.queue_name
    \s+ORDER\s+BY\s+interaction_count\s+DESC
    (?:\s*,\s*q\.queue_name\s+ASC)?
    \s*;?\s*
    """,
    re.IGNORECASE | re.VERBOSE,
)


def extract_q003_date_bounds(sql):
    if inspect_sql(sql) is not True:
        return None

    match = Q003_PATTERN.fullmatch(sql.strip())

    if match is None:
        return None

    try:
        start_date = date.fromisoformat(match.group("start"))
        end_date = date.fromisoformat(match.group("end"))
    except ValueError:
        return None

    try:
        tree = sqlglot.parse_one(sql, read="postgres")
    except sqlglot.errors.ParseError:
        return None

    if tree.find(exp.Limit) is not None:
        return None

    return start_date, end_date