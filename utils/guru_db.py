import sqlite3

def get_conn():
    return sqlite3.connect("labkom.db", check_same_thread=False)

def migrate_guru():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS guru (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            mapel TEXT NOT NULL
        )
    """)
    conn.commit()

def insert_guru(nama, mapel):
    conn = get_conn()
    conn.execute("INSERT INTO guru (nama, mapel) VALUES (?, ?)", (nama, mapel))
    conn.commit()

def get_all_guru():
    conn = get_conn()
    return conn.execute("SELECT * FROM guru").fetchall()

def delete_guru(guru_id):
    conn = get_conn()
    conn.execute("DELETE FROM guru WHERE id = ?", (guru_id,))
    conn.commit()

# Panggil migrasi saat import
migrate_guru()
