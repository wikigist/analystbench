import psycopg

with psycopg.connect("dbname=analystbench") as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM contact_events;")
        result = cursor.fetchone()
        contact_count = result[0]

print(contact_count)