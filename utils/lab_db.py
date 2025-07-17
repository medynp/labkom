import sqlite3

def get_conn():
    return sqlite3.connect("labkom.db", check_same_thread=False)

def migrate_lab():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lab TEXT NOT NULL
        )
    """)
    conn.commit()

def insert_lab(nama_lab):
    conn = get_conn()
    conn.execute("INSERT INTO lab (nama_lab) VALUES (?)", (nama_lab,))
    conn.commit()

def get_all_lab():
    conn = get_conn()
    return conn.execute("SELECT * FROM lab").fetchall()

def delete_lab(lab_id):
    conn = get_conn()
    conn.execute("DELETE FROM lab WHERE id = ?", (lab_id,))
    conn.commit()

# Panggil migrasi saat modul diimpor
migrate_lab()
