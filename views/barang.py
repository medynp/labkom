import streamlit as st
import pandas as pd
from datetime import date
from utils.lab_db import get_all_lab
from utils.barang_db import *

def show_add_barang_section():
    """Menampilkan section untuk tambah barang baru"""
    st.markdown("### Tambah Barang Baru")
    
    lab_list = get_all_lab()
    lab_options = {lab[1]: lab[0] for lab in lab_list}
    
    with st.form("form_tambah_barang"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Barang")
            jumlah = st.number_input("Jumlah", min_value=1)
            kondisi = st.selectbox("Kondisi", ["Baik", "Rusak", "Perlu Perbaikan"])
        
        with col2:
            status = st.selectbox("Status", ["tersedia", "digunakan", "maintenance"])
            kategori = st.text_input("Kategori Barang")
            lab_nama = st.selectbox("Laboratorium", list(lab_options.keys()))

        if st.form_submit_button("Tambah Barang", type="primary"):
            if nama and kategori:
                insert_barang(nama, jumlah, kondisi, status, kategori, lab_options[lab_nama])
                st.success("Barang berhasil ditambahkan.")
                st.rerun()
            else:
                st.error("Nama barang dan kategori harus diisi!")

def show_import_section():
    """Menampilkan section untuk import data barang"""
    st.markdown("### Import Data dari Excel")
    
    # Download template
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. Download Template**")
        template_data = create_import_template()
        st.download_button(
            label="📄 Download Template Excel",
            data=template_data,
            file_name="template_import_barang.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        st.markdown("**2. Upload File**")
        uploaded_file = st.file_uploader(
            "Pilih file Excel",
            type=['xlsx', 'xls'],
            help="Upload file Excel yang sudah diisi sesuai template"
        )
    
    if uploaded_file is not None:
        try:
            # Baca file Excel
            df = pd.read_excel(uploaded_file)
            
            st.success(f"File berhasil dibaca! Ditemukan {len(df)} baris data.")
            
            # Preview data
            st.markdown("**Preview Data:**")
            st.dataframe(df.head(10), use_container_width=True)
            
            if len(df) > 10:
                st.info(f"Menampilkan 10 dari {len(df)} baris.")
            
            # Validasi sederhana
            required_columns = ['nama_barang', 'jumlah', 'kondisi', 'status', 'kategori', 'laboratorium']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Kolom yang hilang: {', '.join(missing_columns)}")
            else:
                st.success("✅ Format file sesuai template")
                
                if st.button("🚀 Import Data", type="primary"):
                    # Proses import sederhana
                    success_count = 0
                    errors = []
                    
                    # Get lab options untuk mapping
                    lab_list = get_all_lab()
                    lab_mapping = {lab[1]: lab[0] for lab in lab_list}
                    
                    for idx, row in df.iterrows():
                        try:
                            # Validasi lab exists
                            if row['laboratorium'] not in lab_mapping:
                                errors.append(f"Baris {idx+2}: Lab '{row['laboratorium']}' tidak ditemukan")
                                continue
                            
                            # Insert data
                            insert_barang(
                                nama=str(row['nama_barang']),
                                jumlah=int(row['jumlah']),
                                kondisi=row['kondisi'],
                                status=row['status'],
                                kategori=str(row['kategori']),
                                lab_id=lab_mapping[row['laboratorium']]
                            )
                            success_count += 1
                            
                        except Exception as e:
                            errors.append(f"Baris {idx+2}: {str(e)}")
                    
                    # Tampilkan hasil
                    if success_count > 0:
                        st.success(f"✅ Berhasil import {success_count} data!")
                    
                    if errors:
                        st.error("❌ Error saat import:")
                        for error in errors[:5]:  # Tampilkan max 5 error
                            st.error(f"• {error}")
                        if len(errors) > 5:
                            st.error(f"... dan {len(errors)-5} error lainnya")
                    
                    if success_count > 0:
                        st.rerun()
                        
        except Exception as e:
            st.error(f"Error membaca file: {str(e)}")

def show_edit_barang_section():
    """Menampilkan section untuk edit barang"""
    st.markdown("### ✏️ Edit Data Barang")

    data = get_all_barang()
    if not data:
        st.info("Belum ada data barang untuk diedit.")
        return

    # Pilih barang yang ingin diedit
    selected = st.selectbox(
        "Pilih Barang",
        options=data,
        format_func=lambda x: f"{x[1]} - {x[6]} ({x[2]} unit) - {x[3]}"
    )

    # Dapatkan data lab
    lab_list = get_all_lab()
    lab_options = {lab[1]: lab[0] for lab in lab_list}
    reverse_lab_options = {v: k for k, v in lab_options.items()}

    # Form edit
    with st.form("form_edit_barang"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Barang", value=selected[1])
            jumlah = st.number_input("Jumlah", min_value=1, value=selected[2])
            kondisi = st.selectbox("Kondisi", ["Baik", "Rusak", "Perlu Perbaikan"], index=["Baik", "Rusak", "Perlu Perbaikan"].index(selected[3]))
        with col2:
            status = st.selectbox("Status", ["tersedia", "digunakan", "maintenance"], index=["tersedia", "digunakan", "maintenance"].index(selected[4]))
            kategori = st.text_input("Kategori Barang", value=selected[5])
            lab_nama = st.selectbox("Laboratorium", list(lab_options.keys()), index=list(lab_options.keys()).index(selected[6]))

        if st.form_submit_button("💾 Simpan Perubahan"):
            from utils.barang_db import update_barang
            update_barang(
                id_barang=selected[0],
                nama=nama,
                jumlah=jumlah,
                kondisi=kondisi,
                status=status,
                kategori=kategori,
                lab_id=lab_options[lab_nama]
            )
            st.success("Data barang berhasil diperbarui.")
            st.rerun()

def show_barang_list_section():
    """Menampilkan section untuk daftar barang dengan filter"""
    st.markdown("### Daftar Barang")
    
    data = get_all_barang()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama Barang", "Jumlah", "Kondisi", "Status", "Kategori", "Laboratorium"])
        
        # Export button di bagian atas
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Total: {len(df)} barang**")
        with col2:
            excel_data = export_barang_to_excel(data=data)
            st.download_button(
                label="📥 Export Excel",
                data=excel_data,
                file_name=f"barang_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        st.divider()
        
        # Filter section
        st.markdown("**🔍 Filter Data:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            kondisi_options = ["Semua"] + list(df["Kondisi"].unique())
            selected_kondisi = st.selectbox("Filter Kondisi", kondisi_options)
        
        with col2:
            status_options = ["Semua"] + list(df["Status"].unique())
            selected_status = st.selectbox("Filter Status", status_options)
        
        with col3:
            lab_options_filter = ["Semua"] + list(df["Laboratorium"].unique())
            selected_lab = st.selectbox("Filter Laboratorium", lab_options_filter)
        
        # Search
        search_name = st.text_input("🔍 Cari berdasarkan nama barang")
        
        # Apply filters
        filtered_df = df.copy()
        
        if selected_kondisi != "Semua":
            filtered_df = filtered_df[filtered_df["Kondisi"] == selected_kondisi]
        
        if selected_status != "Semua":
            filtered_df = filtered_df[filtered_df["Status"] == selected_status]
        
        if selected_lab != "Semua":
            filtered_df = filtered_df[filtered_df["Laboratorium"] == selected_lab]
        
        if search_name:
            filtered_df = filtered_df[filtered_df["Nama Barang"].str.contains(search_name, case=False, na=False)]
        
        st.divider()
        
        # Display filtered results
        if len(filtered_df) != len(df):
            st.info(f"Menampilkan {len(filtered_df)} dari {len(df)} barang")
        
        # Display table without ID column
        display_df = filtered_df.drop(columns=["ID"])
        st.dataframe(display_df, use_container_width=True)
        
        # Quick stats
        if len(filtered_df) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Item", len(filtered_df))
            
            with col2:
                total_qty = filtered_df["Jumlah"].sum()
                st.metric("Total Quantity", total_qty)
            
            with col3:
                tersedia_count = len(filtered_df[filtered_df["Status"] == "tersedia"])
                st.metric("Tersedia", tersedia_count)
            
            with col4:
                baik_count = len(filtered_df[filtered_df["Kondisi"] == "Baik"])
                st.metric("Kondisi Baik", baik_count)
    else:
        st.info("Belum ada data barang. Silakan tambah barang baru atau import data.")

def show_delete_barang_section():
    """Menampilkan section untuk hapus barang"""
    st.markdown("### Hapus Barang")
    
    data = get_all_barang()
    
    if data:
        st.warning("⚠️ **Peringatan:** Tindakan hapus tidak dapat dibatalkan!")
        
        # Filter untuk dropdown hapus
        df = pd.DataFrame(data, columns=["ID", "Nama Barang", "Jumlah", "Kondisi", "Status", "Kategori", "Laboratorium"])
        
        # Filter berdasarkan lab untuk memudahkan pencarian
        lab_for_delete = st.selectbox(
            "Filter berdasarkan Laboratorium (opsional)",
            ["Semua Lab"] + list(df["Laboratorium"].unique()),
            key="delete_lab_filter"
        )
        
        if lab_for_delete != "Semua Lab":
            filtered_data_for_delete = [
                item for item in data 
                if item[6] == lab_for_delete  # index 6 adalah Laboratorium
            ]
        else:
            filtered_data_for_delete = data
        
        if filtered_data_for_delete:
            selected = st.selectbox(
                "Pilih Barang untuk Dihapus",
                options=filtered_data_for_delete,
                format_func=lambda x: f"{x[1]} - {x[6]} ({x[2]} unit) - {x[3]}"
            )
            
            # Tampilkan detail barang yang akan dihapus
            if selected:
                st.info(f"""
                **Detail Barang yang akan dihapus:**
                - **Nama:** {selected[1]}
                - **Jumlah:** {selected[2]} unit
                - **Kondisi:** {selected[3]}
                - **Status:** {selected[4]}
                - **Kategori:** {selected[5]}
                - **Laboratorium:** {selected[6]}
                """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Hapus Barang", type="secondary", use_container_width=True):
                    delete_barang(selected[0])
                    st.success(f"Barang '{selected[1]}' berhasil dihapus.")
                    st.rerun()
            
            with col2:
                if st.button("❌ Batal", use_container_width=True):
                    st.info("Penghapusan dibatalkan.")
        else:
            st.info("Tidak ada barang yang dapat dihapus dari filter yang dipilih.")
    else:
        st.info("Belum ada data barang untuk dihapus.")

def show_statistics_section():
    """Menampilkan section untuk statistik barang"""
    st.markdown("### Statistik Barang")
    
    data = get_all_barang()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama Barang", "Jumlah", "Kondisi", "Status", "Kategori", "Laboratorium"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Distribusi Kondisi Barang:**")
            kondisi_counts = df["Kondisi"].value_counts()
            st.bar_chart(kondisi_counts)
        
        with col2:
            st.markdown("**Distribusi Status Barang:**")
            status_counts = df["Status"].value_counts()
            st.bar_chart(status_counts)
        
        st.divider()
        
        # Tabel summary per lab
        st.markdown("**Summary per Laboratorium:**")
        lab_summary = df.groupby('Laboratorium').agg({
            'Nama Barang': 'count',
            'Jumlah': 'sum'
        }).rename(columns={
            'Nama Barang': 'Jumlah Item',
            'Jumlah': 'Total Quantity'
        })
        
        st.dataframe(lab_summary, use_container_width=True)
        
        # Summary per kategori
        st.divider()
        st.markdown("**Summary per Kategori:**")
        kategori_summary = df.groupby('Kategori').agg({
            'Nama Barang': 'count',
            'Jumlah': 'sum'
        }).rename(columns={
            'Nama Barang': 'Jumlah Item',
            'Jumlah': 'Total Quantity'
        })
        
        st.dataframe(kategori_summary, use_container_width=True)
        
    else:
        st.info("Belum ada data untuk ditampilkan statistik.")

def show_peminjaman_section():
    st.markdown("### 📦 Peminjaman Barang")

    barang_tersedia = [
        b for b in get_all_barang() 
        if b[4] == "tersedia" and b[2] > 0  # pastikan kondisi dan jumlah
    ]

    if not barang_tersedia:
        st.info("Tidak ada barang tersedia untuk dipinjam.")
        return

    # Buat dictionary dengan label unik
    barang_dict = {
        f"{b[1]} | tersedia: {b[2]} | kondisi: {b[3]}": b for b in barang_tersedia
    }

    with st.form("form_peminjaman"):
        peminjam = st.text_input("Nama Peminjam")
        kelas = st.text_input("Kelas")
        label_barang = st.selectbox("Pilih Barang", list(barang_dict.keys()))
        barang = barang_dict[label_barang]

        jumlah = st.number_input(
            "Jumlah Dipinjam", 
            min_value=1, 
            max_value=barang[2],  # jumlah tersedia
            step=1
        )

        keterangan = st.text_area("Keterangan Penggunaan")
        tanggal = st.date_input("Tanggal Peminjaman", value=date.today())

        if st.form_submit_button("Pinjam"):
            insert_peminjaman(
                peminjam, kelas, barang[0], jumlah, keterangan, tanggal.strftime("%Y-%m-%d")
            )
            st.success("Barang berhasil dipinjam.")
            st.rerun()

def show_barang_management():
    """Fungsi utama untuk manajemen barang"""
    st.subheader("🧰 Manajemen Barang Praktik")

    # 1. Tambah Barang Baru
    with st.expander("➕ Tambah Barang Baru", expanded=False):
        show_add_barang_section()

    with st.expander("Edit Barang", expanded=False):
        show_edit_barang_section()
    
    with st.expander("📦 Peminjaman Barang", expanded=False):
        show_peminjaman_section()

    # 2. Import Data
    with st.expander("📥 Import Data Barang", expanded=False):
        show_import_section()

    # 3. Daftar Barang (default terbuka)
    with st.expander("📋 Daftar Barang", expanded=True):
        show_barang_list_section()

    # 4. Hapus Barang
    with st.expander("🗑️ Hapus Barang", expanded=False):
        show_delete_barang_section()
