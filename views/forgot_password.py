import streamlit as st
from auth.auth_service import reset_password

def show_forgot_password():
    st.header("🔁 Reset Password")
    with st.form("forgot_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        new_password = st.text_input("Password Baru", type="password")
        confirm = st.text_input("Konfirmasi Password Baru", type="password")
        submitted = st.form_submit_button("Reset Password")
        if submitted:
            if new_password != confirm:
                st.error("Password baru tidak cocok.")
            else:
                result = reset_password(username, email, new_password)
                if result == "ok":
                    st.success("Password berhasil direset.")
                else:
                    st.error(result)
