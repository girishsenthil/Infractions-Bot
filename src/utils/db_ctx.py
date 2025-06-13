import sqlite3
from contextlib import contextmanager
from utils.config import DB_FILE


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise(e)
    finally:
        conn.close