import sqlglot

def inspect_sql(sql):
    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError:
        print("REJECT: Invalid SQL syntax")
        return False

    print("Statements found:", len(statements))

    if len(statements) != 1:
        print("REJECT: Expected exactly one SQL statement")
        return False

    for statement in statements:
        print("Statement type:", type(statement).__name__)

        # First, check the SQL statement type
        if not isinstance(statement, sqlglot.exp.Select):
            print("REJECT: Only SELECT statements are allowed")
            return False

        # Next, inspect functions inside the SELECT
        for function in statement.find_all(sqlglot.exp.Anonymous):
            print("Function found:", function.name)

            if function.name.lower() == "pg_sleep":
                print("REJECT: pg_sleep is not allowed")
                return False

    # Only reached if all the checks above pass
    return True

if __name__ == "__main__":
    print("Decision:", inspect_sql("SELECT COUNT(*) FROM contact_events;"))

    print("Decision:", inspect_sql("DELETE FROM contact_events;"))

    print("Decision:", inspect_sql("SELECT pg_sleep(10);"))

    print("Decision:", inspect_sql(
        "SELECT COUNT(*) FROM contact_events; "
        "DELETE FROM contact_events;"
    ))