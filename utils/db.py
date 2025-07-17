import sqlite3
import hashlib
import os

DB_NAME = "labkom.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def migrate():
    conn = get_conn()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.commit()

def create_admin():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            ("admin", "admin@example.com", hash_password("admin123"), "admin")
        )
        conn.commit()

# Panggil migrasi dan seed admin saat import
migrate()
create_admin()
