import streamlit as st
import pandas as pd
from utils.barang_db import get_all_barang, update_status_barang, update_kondisi_barang
from utils.formatter import format_tanggal_indo
from utils.maintenance_db import (
    tambah_kerusakan,
    selesaikan_kerusakan,
    get_kerusakan_aktif,
    get_riwayat_kerusakan
)

def show_maintenance_management():
    st.subheader("🛠️ Manajemen Maintenance Barang")

    data = get_all_barang()
    barang_tersedia = [b for b in data if b[4] == "tersedia"]
    barang_maintenance = [b for b in data if b[4] == "maintenance"]

    # Tandai Maintenance
    st.markdown("### ✅ Tandai Barang Maintenance")
    if barang_tersedia:
        selected = st.selectbox(
            "Pilih Barang untuk Dimaintenance",
            options=barang_tersedia,
            format_func=lambda x: f"{x[1]} - {x[6]} ({x[2]} unit)"
        )
        with st.form("form_maintenance"):
            kondisi = st.selectbox("Kondisi Saat Ini", ["Baik", "Perlu Perbaikan", "Rusak"])
            catatan = st.text_area("Catatan Kerusakan")
            if st.form_submit_button("🛠️ Tandai Maintenance"):
                update_kondisi_barang(selected[0], kondisi)
                update_status_barang(selected[0], "maintenance")
                tambah_kerusakan(selected[0], catatan)
                st.success(f"Barang '{selected[1]}' dalam status maintenance.")
                st.rerun()
    else:
        st.info("Tidak ada barang tersedia untuk maintenance.")

    st.markdown("---")

    # Selesaikan Maintenance
    st.markdown("### 🔁 Selesaikan Maintenance")
    if barang_maintenance:
        selected_done = st.selectbox(
            "Pilih Barang Maintenance",
            options=barang_maintenance,
            format_func=lambda x: f"{x[1]} - {x[6]} ({x[2]} unit)",
            key="selesai_maintenance"
        )
        with st.form("form_selesai_maintenance"):
            kondisi_akhir = st.selectbox("Kondisi Setelah Maintenance", ["Baik", "Perlu Perbaikan", "Rusak"])
            catatan_kondisi_akhir = st.text_area("Catatan Tambahan (opsional)")
            if st.form_submit_button("✅ Selesaikan"):
                update_kondisi_barang(selected_done[0], kondisi_akhir)
                update_status_barang(selected_done[0], "tersedia")
                selesaikan_kerusakan(selected_done[0], kondisi_akhir, catatan_kondisi_akhir)
                st.success(f"Barang '{selected_done[1]}' kembali tersedia.")
                st.rerun()
    else:
        st.info("Tidak ada barang dalam maintenance.")

    st.markdown("---")

    # Riwayat Maintenance
    st.markdown("### 📚 Riwayat Maintenance Barang")
    riwayat = get_riwayat_kerusakan()
    if riwayat:
        df = pd.DataFrame(riwayat, columns=[
            "Nama Barang", "Tanggal Mulai", "Tanggal Selesai", "Catatan", "Kondisi Akhir", "Catatan Akhir"
        ])
        
        # Format tanggal ke DMY
        df["Tanggal Mulai"] = pd.to_datetime(df["Tanggal Mulai"], format="mixed", errors="coerce").apply(format_tanggal_indo)
        df["Tanggal Selesai"] = pd.to_datetime(df["Tanggal Selesai"], format="mixed", errors="coerce").apply(format_tanggal_indo)

        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada riwayat maintenance.")
