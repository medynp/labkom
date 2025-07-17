import streamlit as st
import pandas as pd
from utils.lab_db import get_all_lab, insert_lab, delete_lab

def show_lab_management():
    st.subheader("🏫 Manajemen Laboratorium")

    with st.form("form_tambah_lab"):
        nama_lab = st.text_input("Nama Laboratorium")
        if st.form_submit_button("Tambah Lab"):
            if nama_lab:
                insert_lab(nama_lab)
                st.success("Lab berhasil ditambahkan.")
                st.rerun()
            else:
                st.warning("Nama lab tidak boleh kosong.")

    st.markdown("---")
    st.subheader("📋 Daftar Laboratorium")

    data = get_all_lab()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nama Laboratorium"])
        st.dataframe(df[["Nama Laboratorium"]], use_container_width=True)

        selected = st.selectbox(
            "Pilih Lab untuk Dihapus",
            options=data,
            format_func=lambda x: f"{x[1]}"
        )
        if st.button("🗑️ Hapus Lab Terpilih"):
            delete_lab(selected[0])
            st.success(f"Lab '{selected[1]}' berhasil dihapus.")
            st.rerun()
    else:
        st.info("Belum ada data laboratorium.")
