import sqlglot


def inspect_sql(sql):
    statements = sqlglot.parse(sql, read="postgres")

    print("Statements found:", len(statements))

    if len(statements) != 1:
        print("REJECT: Expected exactly one SQL statement")
        return

    for statement in statements:
        print("Statement type:", type(statement).__name__)


if __name__ == "__main__":
    inspect_sql("SELECT COUNT(*) FROM contact_events;")

    inspect_sql("DELETE FROM contact_events;")

    inspect_sql(
        "SELECT COUNT(*) FROM contact_events; "
        "DELETE FROM contact_events;"
    )