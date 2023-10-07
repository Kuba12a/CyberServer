import os
import sqlite3

DB_NAME = "cyb.db"

SETUP_AGENTS_SQL = "CREATE TABLE IF NOT EXISTS agents (" \
                    "id INTEGER PRIMARY KEY," \
                    "ip_address TEXT NOT NULL," \
                    "created_at TEXT DEFAULT CURRENT_TIMESTAMP," \
                    "encryption_key TEXT NOT NULL," \
                    "status TEXT CHECK( status IN (\'added\',\'connected\') ) NOT NULL DEFAULT \'added\'," \
                    "cookie TEXT NOT NULL," \
                    "UNIQUE (ip_address))"


def setup_database():
    connection = connect_to_db()
    connection_cursor = connection.cursor()
    with connection:
        connection_cursor.execute(SETUP_AGENTS_SQL)


def connect_to_db():
    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, DB_NAME)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

