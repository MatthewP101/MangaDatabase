# sqlite3 is included with python
import sqlite3
from pathlib import Path


# file locations
database_file = Path("manga.db")
queries_file = Path("queries.sql")


# make sure the required files exist
if not database_file.exists():
    print("manga.db was not found")
    raise SystemExit

if not queries_file.exists():
    print("queries.sql was not found")
    raise SystemExit


# connect to the manga database
connection = sqlite3.connect(database_file)

try:
    cursor = connection.cursor()

    # read every query from queries.sql
    sql_text = queries_file.read_text(encoding="utf-8")

    # separate each query using the semicolon
    queries = sql_text.split(";")

    query_number = 1

    for query in queries:
        # remove empty space around the query
        query = query.strip()

        # skip empty sections
        if not query:
            continue

        print(f"\n--- query {query_number} ---")

        # run the query
        cursor.execute(query)

        # get the column names
        column_names = [
            description[0]
            for description in cursor.description
        ]

        print(" | ".join(column_names))
        print("-" * 70)

        # print every returned row
        rows = cursor.fetchall()

        for row in rows:
            print(" | ".join(str(value) for value in row))

        # show when no rows were returned
        if not rows:
            print("no results found")

        query_number += 1

except sqlite3.Error as error:
    print(f"database error: {error}")

finally:
    connection.close()