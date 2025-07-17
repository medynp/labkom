import streamlit as st
import pandas as pd
from utils.guru_db import get_all_guru, insert_guru, delete_guru

def show_guru_management():
    st.subheader("👩‍🏫 Manajemen Nama Guru")

    with st.form("form_tambah_guru"):
        nama = st.text_input("Nama Guru")
        mapel = st.text_input("Mata Pelajaran yang Diampu")
        submitted = st.form_submit_button("Tambah Guru")
        if submitted:
            if nama and mapel:
                insert_guru(nama, mapel)
                st.success("Guru berhasil ditambahkan.")
                st.rerun()
            else:
                st.warning("Semua kolom wajib diisi.")

    st.markdown("---")
    st.subheader("📋 Daftar Guru")
    data = get_all_guru()
    if data:
        # Konversi ke DataFrame
        df = pd.DataFrame(data, columns=["ID", "Nama Guru", "Mata Pelajaran"])
        df_display = df[["Nama Guru", "Mata Pelajaran"]]
        st.dataframe(df_display, use_container_width=True)

        # Hapus data
        selected = st.selectbox(
            "Pilih Guru untuk Dihapus",
            options=data,
            format_func=lambda x: f"{x[1]} - {x[2]}",
            index=0 if data else None
        )
        if st.button("🗑️ Hapus Guru Terpilih"):
            delete_guru(selected[0])
            st.success(f"Guru '{selected[1]}' telah dihapus.")
            st.rerun()
    else:
        st.info("Belum ada data guru.")
