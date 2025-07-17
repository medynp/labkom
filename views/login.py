import streamlit as st
from auth.auth_service import login_user
from utils.token_db import create_token
from utils.session import save_token

def show_login():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            token = create_token(user[0])  # simpan token di DB
            user_data = {
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[4]
            }
            save_token(user_data)
            st.session_state.token = token
            st.success(f"Selamat datang, {user[1]}")
            st.rerun()
        else:
            st.error("Login gagal. Periksa kembali username/password.")
