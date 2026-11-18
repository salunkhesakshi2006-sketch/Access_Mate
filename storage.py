import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent.parent / "accessmate.db"

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module TEXT NOT NULL,
            user_input TEXT,
            response TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

def save_interaction(module, user_input, response):
    with connect() as con:
        con.execute(
            "INSERT INTO interactions(module,user_input,response) VALUES(?,?,?)",
            (module, user_input, response)
        )

def get_history(limit=100):
    with connect() as con:
        return con.execute(
            "SELECT module,user_input,response,created_at FROM interactions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

def clear_history():
    with connect() as con:
        con.execute("DELETE FROM interactions")
