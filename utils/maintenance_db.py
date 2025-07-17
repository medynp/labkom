import sqlite3
from datetime import datetime

def get_conn():
    return sqlite3.connect("labkom.db", check_same_thread=False)

def migrate_maintenance():
    conn = get_conn()
    
    # Cek apakah tabel sudah ada
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='maintenance'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Buat tabel baru dengan kolom catatan_kondisi_akhir
        conn.execute("""
            CREATE TABLE maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_barang INTEGER NOT NULL,
                tanggal_mulai TEXT NOT NULL,
                tanggal_selesai TEXT,
                catatan_kerusakan TEXT,
                kondisi_akhir TEXT,
                catatan_kondisi_akhir TEXT,
                status TEXT DEFAULT 'aktif',
                FOREIGN KEY(id_barang) REFERENCES barang(id)
            )
        """)
    else:
        # Cek apakah kolom catatan_kondisi_akhir sudah ada
        cursor = conn.execute("PRAGMA table_info(maintenance)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'catatan_kondisi_akhir' not in columns:
            # Tambahkan kolom catatan_kondisi_akhir jika belum ada
            conn.execute("ALTER TABLE maintenance ADD COLUMN catatan_kondisi_akhir TEXT DEFAULT ''")
        
        if 'status' not in columns:
            # Tambahkan kolom status jika belum ada
            conn.execute("ALTER TABLE maintenance ADD COLUMN status TEXT DEFAULT 'aktif'")
    
    conn.commit()
    conn.close()

def tambah_kerusakan(id_barang, catatan_kerusakan):
    """Menambahkan data kerusakan/maintenance baru"""
    conn = get_conn()
    tanggal_mulai = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO maintenance (id_barang, tanggal_mulai, catatan_kerusakan, status) VALUES (?, ?, ?, 'aktif')",
        (id_barang, tanggal_mulai, catatan_kerusakan)
    )
    conn.commit()
    conn.close()

def selesaikan_kerusakan(id_barang, kondisi_akhir, catatan_akhir=""):
    conn = get_conn()
    conn.execute("""
        UPDATE maintenance SET 
            status = 'selesai',
            tanggal_selesai = ?,
            kondisi_akhir = ?,
            catatan_kondisi_akhir = ?
        WHERE id_barang = ? AND status = 'aktif'
    """, (datetime.now().date(), kondisi_akhir, catatan_akhir, id_barang))
    conn.commit()
    conn.close()

def get_kerusakan_aktif():
    """Mendapatkan daftar maintenance yang masih aktif"""
    conn = get_conn()
    result = conn.execute("""
        SELECT m.id, b.nama_barang, m.tanggal_mulai, m.catatan_kerusakan, m.id_barang
        FROM maintenance m
        LEFT JOIN barang b ON m.id_barang = b.id
        WHERE m.status = 'aktif'
        ORDER BY m.tanggal_mulai DESC
    """).fetchall()
    conn.close()
    return result

def get_riwayat_kerusakan():
    """Mendapatkan riwayat maintenance yang sudah selesai"""
    conn = get_conn()
    result = conn.execute("""
        SELECT b.nama_barang, m.tanggal_mulai, m.tanggal_selesai, m.catatan_kerusakan, 
               m.kondisi_akhir, m.catatan_kondisi_akhir
        FROM maintenance m
        LEFT JOIN barang b ON m.id_barang = b.id
        WHERE m.status = 'selesai'
        ORDER BY m.tanggal_selesai DESC
    """).fetchall()
    conn.close()
    return result

def get_all_maintenance():
    """Mendapatkan semua data maintenance (aktif dan selesai)"""
    conn = get_conn()
    result = conn.execute("""
        SELECT m.id, b.nama_barang, m.tanggal_mulai, m.tanggal_selesai, m.catatan_kerusakan, 
               m.kondisi_akhir, m.catatan_kondisi_akhir, m.status, m.id_barang
        FROM maintenance m
        LEFT JOIN barang b ON m.id_barang = b.id
        ORDER BY m.tanggal_mulai DESC
    """).fetchall()
    conn.close()
    return result

def get_maintenance_by_barang(id_barang):
    """Mendapatkan riwayat maintenance berdasarkan barang"""
    conn = get_conn()
    result = conn.execute("""
        SELECT m.id, b.nama_barang, m.tanggal_mulai, m.tanggal_selesai, m.catatan_kerusakan, 
               m.kondisi_akhir, m.catatan_kondisi_akhir, m.status
        FROM maintenance m
        LEFT JOIN barang b ON m.id_barang = b.id
        WHERE m.id_barang = ?
        ORDER BY m.tanggal_mulai DESC
    """, (id_barang,)).fetchall()
    conn.close()
    return result

def update_maintenance_full(id_maintenance, catatan_kerusakan, kondisi_akhir="", catatan_kondisi_akhir=""):
    """Update data maintenance secara lengkap"""
    conn = get_conn()
    conn.execute("""
        UPDATE maintenance 
        SET catatan_kerusakan = ?, kondisi_akhir = ?, catatan_kondisi_akhir = ?
        WHERE id = ?
    """, (catatan_kerusakan, kondisi_akhir, catatan_kondisi_akhir, id_maintenance))
    conn.commit()
    conn.close()

def delete_maintenance(id_maintenance):
    """Menghapus data maintenance"""
    conn = get_conn()
    conn.execute("DELETE FROM maintenance WHERE id = ?", (id_maintenance,))
    conn.commit()
    conn.close()

def get_statistik_maintenance():
    """Mendapatkan statistik maintenance"""
    conn = get_conn()
    
    # Total maintenance
    total_maintenance = conn.execute("SELECT COUNT(*) FROM maintenance").fetchone()[0]
    
    # Maintenance aktif
    maintenance_aktif = conn.execute("SELECT COUNT(*) FROM maintenance WHERE status = 'aktif'").fetchone()[0]
    
    # Maintenance selesai
    maintenance_selesai = conn.execute("SELECT COUNT(*) FROM maintenance WHERE status = 'selesai'").fetchone()[0]
    
    # Barang paling sering maintenance
    barang_sering_maintenance = conn.execute("""
        SELECT b.nama_barang, COUNT(*) as jumlah
        FROM maintenance m
        LEFT JOIN barang b ON m.id_barang = b.id
        GROUP BY b.nama_barang
        ORDER BY jumlah DESC
        LIMIT 5
    """).fetchall()
    
    # Kondisi akhir paling umum
    kondisi_akhir_umum = conn.execute("""
        SELECT kondisi_akhir, COUNT(*) as jumlah
        FROM maintenance
        WHERE kondisi_akhir IS NOT NULL AND kondisi_akhir != ''
        GROUP BY kondisi_akhir
        ORDER BY jumlah DESC
    """).fetchall()
    
    conn.close()
    
    return {
        'total_maintenance': total_maintenance,
        'maintenance_aktif': maintenance_aktif,
        'maintenance_selesai': maintenance_selesai,
        'barang_sering_maintenance': barang_sering_maintenance,
        'kondisi_akhir_umum': kondisi_akhir_umum
    }

# Jalankan migrasi saat modul diimpor
migrate_maintenance()
