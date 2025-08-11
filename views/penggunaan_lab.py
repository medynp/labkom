import streamlit as st
from datetime import date, datetime
import pandas as pd

from utils.lab_db import get_all_lab
from utils.barang_db import get_all_barang, update_status_barang
from utils.guru_db import get_all_guru
from utils.penggunaan_lab_db import (
    insert_penggunaan_lab,
    get_penggunaan_aktif,
    update_penggunaan_lab_selesai,
    get_riwayat_penggunaan,
    update_penggunaan_lab_full
)
from utils.formatter import format_tanggal_indo

def show_penggunaan_baru_section():
    """Menampilkan section untuk penggunaan lab baru"""
    st.markdown("### Penggunaan Lab Baru")
    
    lab_list = get_all_lab()
    guru_list = get_all_guru()

    if not lab_list or not guru_list:
        st.warning("Pastikan sudah ada data laboratorium dan guru.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_lab = st.selectbox(
                "Laboratorium", 
                options=lab_list, 
                format_func=lambda x: x[1], 
                key="lab_pilih"
            )
            selected_guru = st.selectbox(
                "Guru Pendamping", 
                options=guru_list, 
                format_func=lambda x: f"{x[1]} - {x[2]}", 
                key="guru_pilih"
            )
        
        with col2:
            # Input kelas
            kelas = st.text_input(
                "Kelas",
                placeholder="Contoh: X-1, XI IPA 2, XII TKJ 1",
                key="kelas_input"
            )
            tanggal_mulai = st.date_input(
                "Tanggal Mulai", 
                value=date.today(), 
                key="tgl_mulai"
            )
        
        # Preview informasi
        if selected_lab and selected_guru and kelas:
            st.info(f"""
            **Preview Penggunaan Lab:**
            - **Laboratorium:** {selected_lab[1]}
            - **Guru Pendamping:** {selected_guru[1]} - {selected_guru[2]}
            - **Kelas:** {kelas}
            - **Tanggal Mulai:** {format_tanggal_indo(tanggal_mulai)}
            """)
        
        if st.button("🚀 Gunakan Lab", key="btn_mulai", type="primary", use_container_width=True):
            if kelas.strip():
                insert_penggunaan_lab(selected_lab[0], selected_guru[1], kelas, tanggal_mulai.isoformat())
                barang_di_lab = [b for b in get_all_barang() if b[5] == selected_lab[1] and b[4] == "tersedia"]
                for barang in barang_di_lab:
                    update_status_barang(barang[0], "digunakan")
                st.success(f"✅ Lab '{selected_lab[1]}' digunakan oleh {selected_guru[1]} untuk kelas {kelas} mulai {format_tanggal_indo(tanggal_mulai)}.")
                st.rerun()
            else:
                st.error("Kelas harus diisi!")

def show_selesaikan_penggunaan_section():
    """Menampilkan section untuk selesaikan penggunaan lab"""
    st.markdown("### Selesaikan Penggunaan Lab")
    
    penggunaan_aktif = get_penggunaan_aktif()
    
    if not penggunaan_aktif:
        st.info("Tidak ada penggunaan lab yang aktif.")
    else:
        selected = st.selectbox(
            "Penggunaan Aktif",
            options=penggunaan_aktif,
            format_func=lambda x: f"{format_tanggal_indo(x[4])} - {x[2]} - Kelas {x[3]} (Lab: {x[1]})",
            key="pilih_selesai"
        )
        
        # Preview penggunaan aktif
        if selected:
            st.info(f"""
            **Detail Penggunaan Aktif:**
            - **Laboratorium:** {selected[1]}
            - **Guru Pendamping:** {selected[2]}
            - **Kelas:** {selected[3]}
            - **Tanggal Mulai:** {format_tanggal_indo(selected[4])}
            """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal_selesai = st.date_input(
                "Tanggal Selesai", 
                value=date.today(), 
                key="tgl_selesai"
            )
            kondisi = st.text_input(
                "Kondisi Lab Setelah Digunakan", 
                key="kondisi_selesai",
                placeholder="Contoh: Baik, perlu pembersihan, ada kerusakan, dll"
            )
        
        with col2:
            catatan = st.text_area(
                "Catatan Tambahan", 
                key="catatan_selesai",
                placeholder="Catatan khusus, kendala yang ditemui, saran perbaikan, dll",
                height=100
            )
        
        if st.button("💾 Simpan & Selesaikan", key="btn_selesai", type="primary", use_container_width=True):
            if kondisi.strip():
                update_penggunaan_lab_selesai(selected[0], tanggal_selesai.isoformat(), kondisi, catatan)
                barang_digunakan = [b for b in get_all_barang() if b[5] == selected[1] and b[4] == "digunakan"]
                for barang in barang_digunakan:
                    update_status_barang(barang[0], "tersedia")
                st.success("✅ Berita acara berhasil diselesaikan dan barang direset.")
                st.rerun()
            else:
                st.error("Kondisi lab setelah digunakan harus diisi!")

def show_edit_penggunaan_section():
    """Menampilkan section untuk edit penggunaan lab"""
    st.markdown("### Edit Penggunaan Lab")
    
    riwayat = get_riwayat_penggunaan()
    guru_list = get_all_guru()
    lab_list = get_all_lab()

    if not riwayat or not guru_list or not lab_list:
        st.info("Belum ada data lengkap untuk diedit.")
    else:
        selected = st.selectbox(
            "Riwayat Penggunaan",
            options=riwayat,
            format_func=lambda x: f"{format_tanggal_indo(x[4])} - {x[2]} - Kelas {x[3]} (Lab: {x[1]})",
            key="edit_riwayat"
        )
        
        if selected:
            # Preview data yang akan diedit
            st.info(f"""
            **Data Saat Ini:**
            - **Laboratorium:** {selected[1]}
            - **Guru Pendamping:** {selected[2]}
            - **Kelas:** {selected[3]}
            - **Tanggal Mulai:** {format_tanggal_indo(selected[4])}
            - **Tanggal Selesai:** {format_tanggal_indo(selected[5]) if selected[5] else 'Belum selesai'}
            - **Kondisi:** {selected[6] or 'Belum diisi'}
            - **Catatan:** {selected[7] or 'Belum ada catatan'}
            """)
            
            st.divider()
            st.markdown("**Edit Data:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_lab = st.selectbox(
                    "Edit Lab", 
                    options=lab_list, 
                    format_func=lambda x: x[1], 
                    key="edit_lab"
                )
                selected_guru = st.selectbox(
                    "Edit Guru", 
                    options=guru_list, 
                    format_func=lambda x: f"{x[1]} - {x[2]}", 
                    key="edit_guru"
                )
                kelas_edit = st.text_input(
                    "Edit Kelas",
                    value=selected[3] or "",
                    key="edit_kelas"
                )
            
            with col2:
                tanggal_mulai = st.date_input(
                    "Tanggal Mulai", 
                    value=datetime.strptime(selected[4], "%Y-%m-%d"), 
                    key="edit_mulai"
                )
                tanggal_selesai = st.date_input(
                    "Tanggal Selesai", 
                    value=datetime.strptime(selected[5], "%Y-%m-%d") if selected[5] else date.today(), 
                    key="edit_selesai"
                )
                kondisi = st.text_input(
                    "Kondisi Setelah", 
                    value=selected[6] or "", 
                    key="edit_kondisi"
                )
            
            catatan = st.text_area(
                "Catatan", 
                value=selected[7] or "", 
                key="edit_catatan",
                height=100
            )

            if st.button("💾 Simpan Edit", key="btn_edit", type="primary", use_container_width=True):
                if kelas_edit.strip():
                    update_penggunaan_lab_full(
                        id_penggunaan=selected[0],
                        id_lab=selected_lab[0],
                        guru=selected_guru[1],
                        kelas=kelas_edit,
                        tanggal_mulai=tanggal_mulai.isoformat(),
                        tanggal_selesai=tanggal_selesai.isoformat(),
                        kondisi=kondisi,
                        catatan=catatan
                    )
                    st.success("✅ Data penggunaan lab berhasil diperbarui.")
                    st.rerun()
                else:
                    st.error("Kelas harus diisi!")

def show_riwayat_penggunaan_section():
    """Menampilkan section untuk riwayat penggunaan lab (dengan paginasi & index mulai 1)"""
    st.markdown("### Riwayat Penggunaan Lab")
    
    riwayat = get_riwayat_penggunaan()
    if not riwayat:
        st.info("Belum ada riwayat penggunaan lab.")
        return

    # DataFrame awal
    df = pd.DataFrame(riwayat, columns=[
        "ID", "Laboratorium", "Guru Pendamping", "Kelas", "Tanggal Mulai",
        "Tanggal Selesai", "Kondisi Setelah", "Catatan"
    ])

    # Format tanggal
    df["Tanggal Mulai"] = df["Tanggal Mulai"].apply(format_tanggal_indo)
    df["Tanggal Selesai"] = df["Tanggal Selesai"].apply(format_tanggal_indo)

    # Header + Export
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Total: {len(df)} penggunaan lab**")
    with col2:
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.drop(columns=["ID"]).to_excel(writer, sheet_name='Riwayat_Penggunaan_Lab', index=False)
        output.seek(0)
        st.download_button(
            label="📥 Export Excel",
            data=output.getvalue(),
            file_name=f"riwayat_penggunaan_lab_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.divider()

    # 🔍 Filter
    st.markdown("**🔍 Filter Data:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lab_options = ["Semua"] + sorted(list(df["Laboratorium"].dropna().unique()))
        selected_lab_filter = st.selectbox("Filter Laboratorium", lab_options)
    with col2:
        guru_options = ["Semua"] + sorted(list(df["Guru Pendamping"].dropna().unique()))
        selected_guru_filter = st.selectbox("Filter Guru", guru_options)
    with col3:
        kelas_options = ["Semua"] + sorted(list(df["Kelas"].dropna().unique()))
        selected_kelas_filter = st.selectbox("Filter Kelas", kelas_options)
    with col4:
        status_options = ["Semua", "Sudah Selesai", "Belum Selesai"]
        selected_status = st.selectbox("Filter Status", status_options)

    # Terapkan filter
    filtered_df = df.copy()
    if selected_lab_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Laboratorium"] == selected_lab_filter]
    if selected_guru_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Guru Pendamping"] == selected_guru_filter]
    if selected_kelas_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Kelas"] == selected_kelas_filter]
    if selected_status == "Sudah Selesai":
        filtered_df = filtered_df[filtered_df["Tanggal Selesai"] != ""]
    elif selected_status == "Belum Selesai":
        filtered_df = filtered_df[filtered_df["Tanggal Selesai"] == ""]

    st.divider()

    # Info hasil filter
    if len(filtered_df) != len(df):
        st.info(f"Menampilkan {len(filtered_df)} dari {len(df)} penggunaan lab")

    # ====== 🔢 PAGINASI ======
    import math

    # Reset halaman ketika filter berubah
    filters_signature = (selected_lab_filter, selected_guru_filter, selected_kelas_filter, selected_status)
    if "riwayat_filters_sig" not in st.session_state:
        st.session_state.riwayat_filters_sig = filters_signature
    if st.session_state.riwayat_filters_sig != filters_signature:
        st.session_state.riwayat_filters_sig = filters_signature
        st.session_state.riwayat_page = 1

    # Inisialisasi state page & page size
    if "riwayat_page" not in st.session_state:
        st.session_state.riwayat_page = 1
    if "riwayat_page_size" not in st.session_state:
        st.session_state.riwayat_page_size = 10

    # Kontrol paginasi
    col_a, col_b, col_c, col_d = st.columns([1.2, 1.2, 2, 3])
    with col_a:
        page_size = st.selectbox("Baris/halaman", [10, 20, 30, 50], index=[10,20,30,50].index(st.session_state.riwayat_page_size))
        if page_size != st.session_state.riwayat_page_size:
            st.session_state.riwayat_page_size = page_size
            st.session_state.riwayat_page = 1
    total_rows = len(filtered_df)
    total_pages = max(1, math.ceil(total_rows / st.session_state.riwayat_page_size))

    with col_b:
        # Input nomor halaman
        current_page_input = st.number_input(
            "Halaman",
            min_value=1,
            max_value=total_pages,
            value=st.session_state.riwayat_page,
            step=1
        )
        if current_page_input != st.session_state.riwayat_page:
            st.session_state.riwayat_page = current_page_input
            st.rerun()

    with col_c:
        st.markdown(f"**Total Halaman:** {total_pages}")

    with col_d:
        prev_col, next_col = st.columns(2)
        with prev_col:
            if st.button("◀️ Sebelumnya", disabled=st.session_state.riwayat_page <= 1, use_container_width=True):
                st.session_state.riwayat_page -= 1
                st.rerun()
        with next_col:
            if st.button("Berikutnya ▶️", disabled=st.session_state.riwayat_page >= total_pages, use_container_width=True):
                st.session_state.riwayat_page += 1
                st.rerun()

    # Hitung slice data
    start = (st.session_state.riwayat_page - 1) * st.session_state.riwayat_page_size
    end = start + st.session_state.riwayat_page_size
    page_df = filtered_df.iloc[start:end].drop(columns=["ID"]).copy()

    # Index mulai 1 (berdasarkan posisi global setelah filter)
    page_df.reset_index(drop=True, inplace=True)
    page_df.index = range(start + 1, start + 1 + len(page_df))
    page_df.index.name = "No"

    # Tabel
    st.dataframe(page_df, use_container_width=True)

    # Quick stats
    if len(filtered_df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Penggunaan (terfilter)", len(filtered_df))
        with col2:
            selesai_count = len(filtered_df[filtered_df["Tanggal Selesai"] != ""])
            st.metric("Sudah Selesai", selesai_count)
        with col3:
            aktif_count = len(filtered_df[filtered_df["Tanggal Selesai"] == ""])
            st.metric("Masih Aktif", aktif_count)
        with col4:
            lab_count = len(filtered_df["Laboratorium"].unique())
            st.metric("Lab Digunakan", lab_count)

def show_penggunaan_lab():
    """Fungsi utama untuk berita acara penggunaan laboratorium"""
    st.subheader("📋 Berita Acara Penggunaan Laboratorium")

    # 1. Penggunaan Baru
    with st.expander("🆕 Penggunaan Lab Baru", expanded=False):
        show_penggunaan_baru_section()

    # 2. Selesaikan Penggunaan
    with st.expander("✅ Selesaikan Penggunaan Lab", expanded=False):
        show_selesaikan_penggunaan_section()

    # 3. Edit Penggunaan
    with st.expander("✏️ Edit Penggunaan Lab", expanded=False):
        show_edit_penggunaan_section()

    # 4. Riwayat
    with st.expander("📜 Riwayat Penggunaan Lab", expanded=False):
        show_riwayat_penggunaan_section()
