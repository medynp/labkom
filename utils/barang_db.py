import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from .db import *
def get_conn():
    return sqlite3.connect("labkom.db", check_same_thread=False)

def migrate_barang():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_barang TEXT NOT NULL,
            jumlah INTEGER NOT NULL,
            jumlah_tersedia INTEGER NOT NULL,
            kondisi TEXT NOT NULL,
            status TEXT DEFAULT 'tersedia',
            kategori TEXT,
            lab_id INTEGER,
            FOREIGN KEY(lab_id) REFERENCES lab(id)
        )
    """)
    try:
        conn.execute("ALTER TABLE barang ADD COLUMN kategori TEXT")
    except:
        pass
    conn.commit()

def insert_barang(nama, jumlah, kondisi, status, kategori, lab_id):
    conn = get_conn()
    conn.execute(
        "INSERT INTO barang (nama, jumlah, jumlah_tersedia, kondisi, status, kategori, lab_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nama, jumlah, jumlah, kondisi, status, kategori, lab_id)  # jumlah_tersedia = jumlah
    )
    conn.commit()

def get_all_barang():
    conn = get_conn()
    return conn.execute("""
        SELECT b.id, b.nama_barang, b.jumlah, b.kondisi, b.status, b.kategori, l.nama_lab
        FROM barang b
        LEFT JOIN lab l ON b.lab_id = l.id
    """).fetchall()

def delete_barang(barang_id):
    conn = get_conn()
    conn.execute("DELETE FROM barang WHERE id = ?", (barang_id,))
    conn.commit()

def update_status_barang(barang_id, status):
    conn = get_conn()
    conn.execute("UPDATE barang SET status = ? WHERE id = ?", (status, barang_id))
    conn.commit()

def update_kondisi_barang(barang_id, kondisi):
    conn = get_conn()
    conn.execute("UPDATE barang SET kondisi = ? WHERE id = ?", (kondisi, barang_id))
    conn.commit()

def update_barang(id_barang, nama, jumlah, kondisi, status, kategori, lab_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE barang 
        SET nama = ?, jumlah = ?, kondisi = ?, status = ?, kategori = ?, lab_id = ?
        WHERE id = ?
    """, (nama, jumlah, kondisi, status, kategori, lab_id, id_barang))
    conn.commit()
    conn.close()

# Fungsi yang sudah ada tetap tidak berubah...

def create_import_template():
    """
    Membuat template Excel untuk import barang
    
    Returns:
        bytes: File Excel template
    """
    from io import BytesIO
    
    # Data template
    template_data = {
        'nama_barang': ['Mikroskop Digital', 'Bunsen Burner', 'Beaker Glass 500ml'],
        'jumlah': [5, 10, 20],
        'kondisi': ['Baik', 'Baik', 'Perlu Perbaikan'],
        'status': ['tersedia', 'tersedia', 'maintenance'],
        'kategori': ['Alat Optik', 'Alat Pemanas', 'Glassware'],
        'laboratorium': ['Lab Biologi', 'Lab Kimia', 'Lab Kimia']
    }
    
    df_template = pd.DataFrame(template_data)
    
    # Buat file Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet template
        df_template.to_excel(writer, sheet_name='Template_Barang', index=False)
        
        # Sheet instruksi
        instruksi = pd.DataFrame({
            'Instruksi Penggunaan Template Import Barang': [
                '1. Isi data pada sheet "Template_Barang"',
                '2. Jangan mengubah nama kolom',
                '3. Kolom yang wajib diisi: nama_barang, jumlah, kondisi, status, kategori, laboratorium',
                '4. Kondisi: Baik, Rusak, Perlu Perbaikan',
                '5. Status: tersedia, digunakan, maintenance',
                '6. Pastikan nama laboratorium sudah terdaftar di sistem',
                '7. Jumlah harus berupa angka positif',
                '8. Simpan file dalam format Excel (.xlsx)',
                '9. Upload file melalui menu Import Data'
            ]
        })
        instruksi.to_excel(writer, sheet_name='Instruksi', index=False)
    
    output.seek(0)
    return output.getvalue()

def export_barang_to_excel(data=None, filtered_data=None):
    """
    Export data barang ke Excel
    
    Parameters:
        data: List data barang dari database (optional)
        filtered_data: DataFrame data yang sudah difilter (optional)
    
    Returns:
        bytes: File Excel
    """
    from io import BytesIO
    
    # Jika tidak ada filtered_data, gunakan data atau ambil semua data
    if filtered_data is not None:
        df = filtered_data
    elif data is not None:
        df = pd.DataFrame(data, columns=["ID", "Nama Barang", "Jumlah", "Kondisi", "Status", "Kategori", "Laboratorium"])
    else:
        # Ambil semua data jika tidak ada parameter
        all_data = get_all_barang()
        df = pd.DataFrame(all_data, columns=["ID", "Nama Barang", "Jumlah", "Kondisi", "Status", "Kategori", "Laboratorium"])
    
    # Buat file Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet data utama
        df.to_excel(writer, sheet_name='Data_Barang', index=False)
        
        # Sheet summary
        if len(df) > 0:
            # Summary berdasarkan kondisi
            kondisi_summary = df.groupby('Kondisi').agg({
                'Nama Barang': 'count',
                'Jumlah': 'sum'
            }).rename(columns={'Nama Barang': 'Jumlah Item'})
            
            # Summary berdasarkan status
            status_summary = df.groupby('Status').agg({
                'Nama Barang': 'count',
                'Jumlah': 'sum'
            }).rename(columns={'Nama Barang': 'Jumlah Item'})
            
            # Summary berdasarkan laboratorium
            lab_summary = df.groupby('Laboratorium').agg({
                'Nama Barang': 'count',
                'Jumlah': 'sum'
            }).rename(columns={'Nama Barang': 'Jumlah Item'})
            
            # Tulis summary ke sheet terpisah
            kondisi_summary.to_excel(writer, sheet_name='Summary_Kondisi')
            status_summary.to_excel(writer, sheet_name='Summary_Status')
            lab_summary.to_excel(writer, sheet_name='Summary_Lab')
    
    output.seek(0)
    return output.getvalue()

def insert_peminjaman(nama_peminjam, kelas, id_barang, jumlah_pinjam, keperluan, tanggal_pinjam):
    conn = get_conn()
    cursor = conn.cursor()

    # Simpan ke tabel peminjaman
    cursor.execute("""
        INSERT INTO peminjaman_barang (
            nama_peminjam, kelas_peminjam, id_barang, jumlah_pinjam, keperluan, tanggal_pinjam
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (nama_peminjam, kelas, id_barang, jumlah_pinjam, keperluan, tanggal_pinjam))

    # Update jumlah tersedia di tabel barang
    cursor.execute("SELECT jumlah_tersedia, jumlah FROM barang WHERE id = ?", (id_barang,))
    row = cursor.fetchone()
    if row:
        jumlah_tersisa = row["jumlah_tersedia"] - jumlah_pinjam
        status = "digunakan" if jumlah_tersisa == 0 else "tersedia"
        cursor.execute("UPDATE barang SET jumlah_tersedia = ?, status = ? WHERE id = ?", (jumlah_tersisa, status, id_barang))

    conn.commit()
    conn.close()

def kembalikan_barang(id_peminjaman, catatan_setelah, tanggal_kembali):
    conn = get_conn()
    cursor = conn.cursor()

    # Ambil data peminjaman
    cursor.execute("SELECT id_barang, jumlah_pinjam FROM peminjaman_barang WHERE id = ?", (id_peminjaman,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    id_barang = row["id_barang"]
    jumlah_kembali = row["jumlah_pinjam"]

    # Update jumlah tersedia
    cursor.execute("SELECT jumlah_tersedia, jumlah FROM barang WHERE id = ?", (id_barang,))
    barang = cursor.fetchone()
    if barang:
        tersedia = barang["jumlah_tersedia"] + jumlah_kembali
        status = "tersedia" if tersedia == barang["jumlah"] else "digunakan"
        cursor.execute("UPDATE barang SET jumlah_tersedia = ?, status = ? WHERE id = ?", (tersedia, status, id_barang))

    # Update catatan pengembalian
    cursor.execute("""
        UPDATE peminjaman_barang
        SET tanggal_kembali = ?, catatan_setelah = ?
        WHERE id = ?
    """, (tanggal_kembali, catatan_setelah, id_peminjaman))

    conn.commit()
    conn.close()
    return True

def get_peminjaman_aktif():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pb.id, pb.nama_peminjam, pb.kelas_peminjam, b.nama_barang AS nama_barang,
               pb.jumlah_pinjam, pb.tanggal_pinjam, pb.keperluan
        FROM peminjaman_barang pb
        JOIN barang b ON pb.id_barang = b.id
        WHERE pb.tanggal_kembali IS NULL
    """)
    return cursor.fetchall()

def get_riwayat_peminjaman():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pb.nama_peminjam, pb.kelas_peminjam, b.nama_barang AS nama_barang,
               pb.jumlah_pinjam, pb.tanggal_pinjam, pb.tanggal_kembali, pb.keperluan, pb.catatan_setelah
        FROM peminjaman_barang pb
        JOIN barang b ON pb.id_barang = b.id
        WHERE pb.tanggal_kembali IS NOT NULL
        ORDER BY pb.tanggal_kembali DESC
    """)
    return cursor.fetchall()

migrate_barang()
