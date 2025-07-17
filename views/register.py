import streamlit as st
from auth.auth_service import register_user

def show_register():
    st.header("📝 Registrasi")
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Konfirmasi Password", type="password")
        submitted = st.form_submit_button("Daftar")
        if submitted:
            if password != confirm:
                st.error("Password tidak cocok.")
            else:
                result = register_user(username, email, password)
                if result == "ok":
                    st.success("Registrasi berhasil. Silakan login.")
                else:
                    st.error(f"Gagal: {result}")
