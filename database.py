import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",     # atau 127.0.0.1
        user="root",          # sesuaikan
        password="",          # sesuaikan
        database="labkompy"  # nama database
    )

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id_user INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nama_lengkap VARCHAR(100) NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        )
    """)
    
    conn.commit()
    conn.close()