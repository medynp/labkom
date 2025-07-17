import streamlit as st
from utils.penggunaan_lab_db import get_riwayat_penggunaan, update_penggunaan_lab_selesai
from datetime import datetime

def show_edit_penggunaan_lab():
    st.subheader("✏️ Edit Berita Acara Penggunaan Lab")

    data = get_riwayat_penggunaan()
    if not data:
        st.info("Belum ada data penggunaan lab.")
        return

    selected = st.selectbox(
        "Pilih Data untuk Diedit",
        options=data,
        format_func=lambda x: f"{datetime.strptime(x[3], '%Y-%m-%d').strftime('%d/%m/%Y')} - {x[2]} (Lab: {x[1]})"
    )

    st.markdown("### Form Edit")

    with st.form("edit_form"):
        tanggal_selesai = st.date_input("Tanggal Selesai", value=datetime.strptime(selected[4], "%Y-%m-%d") if selected[4] else datetime.today())
        kondisi = st.text_input("Kondisi Lab Setelah Digunakan", value=selected[5] or "")
        catatan = st.text_area("Catatan Tambahan", value=selected[6] or "")
        submit = st.form_submit_button("Simpan Perubahan")

        if submit:
            update_penggunaan_lab_selesai(
                selected[0], tanggal_selesai.isoformat(), kondisi, catatan
            )
            st.success("Data berhasil diperbarui.")
            st.rerun()
