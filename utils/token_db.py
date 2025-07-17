import sqlite3
import uuid
from datetime import datetime

def get_conn():
    return sqlite3.connect("labkom.db", check_same_thread=False)

def migrate_token_table():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS token_sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()

def create_token(user_id):
    conn = get_conn()
    token = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    conn.execute("INSERT INTO token_sessions (token, user_id, created_at) VALUES (?, ?, ?)",
                 (token, user_id, created_at))
    conn.commit()
    return token

def validate_token(token):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.email, u.role
        FROM token_sessions ts
        JOIN users u ON ts.user_id = u.id
        WHERE ts.token = ?
    """, (token,))
    return cur.fetchone()

def delete_token(token):
    conn = get_conn()
    conn.execute("DELETE FROM token_sessions WHERE token = ?", (token,))
    conn.commit()

# Panggil saat import
migrate_token_table()
