import uuid
import streamlit as st

def generate_token():
    return str(uuid.uuid4())

def save_token(user, token=None):
    if token is None:
        token = generate_token()
    st.session_state.token = token
    st.session_state.user = user
    st.session_state.logged_in = True

def is_authenticated():
    return st.session_state.get("logged_in", False) and "token" in st.session_state

def load_token_from_session():
    return st.session_state.get("token")

def logout():
    for key in ["token", "user", "logged_in"]:
        if key in st.session_state:
            del st.session_state[key]
