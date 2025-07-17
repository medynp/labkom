import sqlite3
from datetime import datetime

def get_conn():
    return sqlite3.connect("labkom.db", check_same_thread=False)

def migrate_penggunaan_lab():
    conn = get_conn()
    
    # Cek apakah tabel sudah ada
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='penggunaan_lab'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Buat tabel baru dengan kolom kelas
        conn.execute("""
            CREATE TABLE penggunaan_lab (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_lab INTEGER NOT NULL,
                guru TEXT NOT NULL,
                kelas TEXT NOT NULL,
                tanggal_mulai TEXT NOT NULL,
                tanggal_selesai TEXT,
                kondisi_setelah TEXT,
                catatan TEXT,
                FOREIGN KEY(id_lab) REFERENCES lab(id)
            )
        """)
    else:
        # Cek apakah kolom kelas sudah ada
        cursor = conn.execute("PRAGMA table_info(penggunaan_lab)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'kelas' not in columns:
            # Tambahkan kolom kelas jika belum ada
            conn.execute("ALTER TABLE penggunaan_lab ADD COLUMN kelas TEXT DEFAULT ''")
            
            # Update existing records dengan kelas default
            conn.execute("UPDATE penggunaan_lab SET kelas = 'Tidak Diketahui' WHERE kelas = '' OR kelas IS NULL")
    
    conn.commit()
    conn.close()

def insert_penggunaan_lab(id_lab, guru, kelas, tanggal_mulai):
    conn = get_conn()
    conn.execute(
        "INSERT INTO penggunaan_lab (id_lab, guru, kelas, tanggal_mulai) VALUES (?, ?, ?, ?)",
        (id_lab, guru, kelas, tanggal_mulai)
    )
    conn.commit()
    conn.close()

def update_penggunaan_lab_selesai(id_penggunaan, tanggal_selesai, kondisi, catatan):
    conn = get_conn()
    conn.execute(
        "UPDATE penggunaan_lab SET tanggal_selesai = ?, kondisi_setelah = ?, catatan = ? WHERE id = ?",
        (tanggal_selesai, kondisi, catatan, id_penggunaan)
    )
    conn.commit()
    conn.close()

def get_riwayat_penggunaan():
    conn = get_conn()
    result = conn.execute("""
        SELECT p.id, l.nama_lab, p.guru, p.kelas, p.tanggal_mulai, p.tanggal_selesai,
               p.kondisi_setelah, p.catatan
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        ORDER BY p.id DESC
    """).fetchall()
    conn.close()
    return result

def get_penggunaan_aktif():
    conn = get_conn()
    result = conn.execute("""
        SELECT p.id, l.nama_lab, p.guru, p.kelas, p.tanggal_mulai
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        WHERE p.tanggal_selesai IS NULL
        ORDER BY p.tanggal_mulai DESC
    """).fetchall()
    conn.close()
    return result

def update_penggunaan_lab_full(id_penggunaan, id_lab, guru, kelas, tanggal_mulai, tanggal_selesai, kondisi, catatan):
    conn = get_conn()
    conn.execute("""
        UPDATE penggunaan_lab
        SET id_lab = ?, guru = ?, kelas = ?, tanggal_mulai = ?, tanggal_selesai = ?, kondisi_setelah = ?, catatan = ?
        WHERE id = ?
    """, (id_lab, guru, kelas, tanggal_mulai, tanggal_selesai, kondisi, catatan, id_penggunaan))
    conn.commit()
    conn.close()

def get_penggunaan_by_id(id_penggunaan):
    """Mendapatkan data penggunaan lab berdasarkan ID"""
    conn = get_conn()
    result = conn.execute("""
        SELECT p.id, l.nama_lab, p.guru, p.kelas, p.tanggal_mulai, p.tanggal_selesai,
               p.kondisi_setelah, p.catatan, p.id_lab
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        WHERE p.id = ?
    """, (id_penggunaan,)).fetchone()
    conn.close()
    return result

def get_penggunaan_by_lab(id_lab):
    """Mendapatkan riwayat penggunaan berdasarkan lab"""
    conn = get_conn()
    result = conn.execute("""
        SELECT p.id, l.nama_lab, p.guru, p.kelas, p.tanggal_mulai, p.tanggal_selesai,
               p.kondisi_setelah, p.catatan
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        WHERE p.id_lab = ?
        ORDER BY p.tanggal_mulai DESC
    """, (id_lab,)).fetchall()
    conn.close()
    return result

def get_penggunaan_by_guru(guru):
    """Mendapatkan riwayat penggunaan berdasarkan guru"""
    conn = get_conn()
    result = conn.execute("""
        SELECT p.id, l.nama_lab, p.guru, p.kelas, p.tanggal_mulai, p.tanggal_selesai,
               p.kondisi_setelah, p.catatan
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        WHERE p.guru = ?
        ORDER BY p.tanggal_mulai DESC
    """, (guru,)).fetchall()
    conn.close()
    return result

def get_penggunaan_by_kelas(kelas):
    """Mendapatkan riwayat penggunaan berdasarkan kelas"""
    conn = get_conn()
    result = conn.execute("""
        SELECT p.id, l.nama_lab, p.guru, p.kelas, p.tanggal_mulai, p.tanggal_selesai,
               p.kondisi_setelah, p.catatan
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        WHERE p.kelas = ?
        ORDER BY p.tanggal_mulai DESC
    """, (kelas,)).fetchall()
    conn.close()
    return result

def get_statistik_penggunaan():
    """Mendapatkan statistik penggunaan lab"""
    conn = get_conn()
    
    # Total penggunaan
    total_penggunaan = conn.execute("SELECT COUNT(*) FROM penggunaan_lab").fetchone()[0]
    
    # Penggunaan aktif
    penggunaan_aktif = conn.execute("SELECT COUNT(*) FROM penggunaan_lab WHERE tanggal_selesai IS NULL").fetchone()[0]
    
    # Penggunaan selesai
    penggunaan_selesai = conn.execute("SELECT COUNT(*) FROM penggunaan_lab WHERE tanggal_selesai IS NOT NULL").fetchone()[0]
    
    # Lab paling sering digunakan
    lab_populer = conn.execute("""
        SELECT l.nama_lab, COUNT(*) as jumlah
        FROM penggunaan_lab p
        LEFT JOIN lab l ON p.id_lab = l.id
        GROUP BY l.nama_lab
        ORDER BY jumlah DESC
        LIMIT 5
    """).fetchall()
    
    # Guru paling aktif
    guru_aktif = conn.execute("""
        SELECT guru, COUNT(*) as jumlah
        FROM penggunaan_lab
        GROUP BY guru
        ORDER BY jumlah DESC
        LIMIT 5
    """).fetchall()
    
    # Kelas paling aktif
    kelas_aktif = conn.execute("""
        SELECT kelas, COUNT(*) as jumlah
        FROM penggunaan_lab
        WHERE kelas != 'Tidak Diketahui'
        GROUP BY kelas
        ORDER BY jumlah DESC
        LIMIT 5
    """).fetchall()
    
    conn.close()
    
    return {
        'total_penggunaan': total_penggunaan,
        'penggunaan_aktif': penggunaan_aktif,
        'penggunaan_selesai': penggunaan_selesai,
        'lab_populer': lab_populer,
        'guru_aktif': guru_aktif,
        'kelas_aktif': kelas_aktif
    }

def delete_penggunaan_lab(id_penggunaan):
    """Menghapus data penggunaan lab"""
    conn = get_conn()
    conn.execute("DELETE FROM penggunaan_lab WHERE id = ?", (id_penggunaan,))
    conn.commit()
    conn.close()

# Jalankan migrasi saat modul diimpor
migrate_penggunaan_lab()
