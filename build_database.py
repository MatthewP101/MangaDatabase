# sqlite3 is included with python
import sqlite3
from pathlib import Path


# database and sql file locations
database_file = Path("manga.db")
schema_file = Path("schema.sql")
sample_data_file = Path("sample_data.sql")


# check that the sql files exist
if not schema_file.exists():
    print("schema.sql was not found")
    raise SystemExit

if not sample_data_file.exists():
    print("sample_data.sql was not found")
    raise SystemExit


# connect to the database
# sqlite creates the file if it does not exist
connection = sqlite3.connect(database_file)

try:
    cursor = connection.cursor()

    # turn on foreign key checks
    cursor.execute("pragma foreign_keys = on;")

    # read and run the database structure
    schema_sql = schema_file.read_text(encoding="utf-8")
    cursor.executescript(schema_sql)

    # read and add the sample data
    sample_data_sql = sample_data_file.read_text(encoding="utf-8")
    cursor.executescript(sample_data_sql)

    # save all database changes
    connection.commit()

    print("manga.db created successfully")

except sqlite3.Error as error:
    # undo changes if something fails
    connection.rollback()
    print(f"database error: {error}")

finally:
    # always close the connection
    connection.close()