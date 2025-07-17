import streamlit as st
from views.login import show_login
from views.register import show_register
from views.forgot_password import show_forgot_password
from views.guru import show_guru_management
from views.lab import show_lab_management
from views.barang import show_barang_management
from views.maintenance import show_maintenance_management
from views.penggunaan_lab import show_penggunaan_lab
from views.edit_penggunaan_lab import show_edit_penggunaan_lab
from utils.session import *
from utils.token_db import validate_token

# Konfigurasi awal Streamlit
st.set_page_config(
    page_title="Sistem Manajemen Lab", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧪"
)

# Inisialisasi session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Token validation
token = load_token_from_session()
if not is_authenticated() and token:
    user = validate_token(token)
    if user:
        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3]
        }
        save_token(user_data, token=token)

# Validasi token dari database
if not is_authenticated() and "token" in st.session_state:
    token = st.session_state.token
    user = validate_token(token)
    if user:
        user_data = {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3]
        }
        save_token(user_data, token=token)

# Halaman utama
if "page" not in st.session_state:
    st.session_state.page = "login"

# Menu items dengan icons
MENU_ITEMS = [
    {"key": "Dashboard", "icon": "🏠", "label": "Dashboard"},
    {"key": "Manajemen Guru", "icon": "👨‍🏫", "label": "Manajemen Guru"},
    {"key": "Manajemen Lab", "icon": "🧪", "label": "Manajemen Lab"},
    {"key": "Manajemen Barang", "icon": "📦", "label": "Manajemen Barang"},
    {"key": "Maintenance Barang", "icon": "🔧", "label": "Maintenance Barang"},
    {"key": "Penggunaan Lab", "icon": "📊", "label": "Penggunaan Lab"}
]

# Jika sudah login
if is_authenticated():
    with st.sidebar:
        # Header sidebar
        st.title("🧭 Navigasi Sistem")
        
        # User info
        with st.container():
            st.success(f"👤 **{st.session_state.user['username']}**")
            st.caption(f"Role: {st.session_state.user.get('role', 'User')}")
        
        st.divider()
        
        # Navigation menggunakan button dalam container
        st.subheader("📋 Menu Utama")
        
        for item in MENU_ITEMS:
            # Highlight current page
            button_type = "primary" if st.session_state.current_page == item["key"] else "secondary"
            
            if st.button(
                f"{item['icon']} {item['label']}", 
                key=f"nav_{item['key']}", 
                use_container_width=True,
                type=button_type
            ):
                st.session_state.current_page = item["key"]
                st.rerun()
        
        st.divider()
        
        # Quick info section
        with st.expander("ℹ️ Informasi Sistem"):
            st.info("**Versi:** 1.0.0")
            st.info("**Status:** 🟢 Online")
            st.info("**Update:** Hari ini")
        
        # Logout section
        st.divider()
        if st.button("🔓 Logout", type="secondary", use_container_width=True):
            from utils.token_db import delete_token
            if "token" in st.session_state:
                delete_token(st.session_state.token)
            logout()
            st.rerun()

    # Main content area
    st.title("🧪 Sistem Manajemen Praktik & Guru")
    st.caption("Platform terpadu untuk mengelola laboratorium dan sumber daya pendidikan")
    
    # Breadcrumb
    st.markdown(f"**📍 Lokasi:** {st.session_state.current_page}")
    st.divider()

    # Content routing berdasarkan current_page
    current_page = st.session_state.current_page
    
    if current_page == "Dashboard":
        st.header("🏠 Dashboard")
        
        # Metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👨‍🏫 Total Guru",
                value="25",
                delta="2 baru minggu ini"
            )
        
        with col2:
            st.metric(
                label="🧪 Total Lab",
                value="8",
                delta="1 dalam maintenance"
            )
        
        with col3:
            st.metric(
                label="📦 Total Barang",
                value="150",
                delta="5 perlu maintenance"
            )
        
        with col4:
            st.metric(
                label="📊 Penggunaan Hari Ini",
                value="12",
                delta="3 dari kemarin"
            )
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Aksi Cepat")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("➕ Tambah Guru", use_container_width=True):
                st.session_state.current_page = "Manajemen Guru"
                st.rerun()
        
        with col2:
            if st.button("🧪 Kelola Lab", use_container_width=True):
                st.session_state.current_page = "Manajemen Lab"
                st.rerun()
        
        with col3:
            if st.button("📦 Tambah Barang", use_container_width=True):
                st.session_state.current_page = "Manajemen Barang"
                st.rerun()
        
        with col4:
            if st.button("📊 Lihat Laporan", use_container_width=True):
                st.session_state.current_page = "Penggunaan Lab"
                st.rerun()
        
        st.divider()
        
        
    elif current_page == "Manajemen Guru":
        show_guru_management()
    elif current_page == "Manajemen Lab":
        show_lab_management()
    elif current_page == "Manajemen Barang":
        show_barang_management()
    elif current_page == "Maintenance Barang":
        show_maintenance_management()
    elif current_page == "Penggunaan Lab":
        show_penggunaan_lab()
    elif current_page == "Monitoring PC":
        show_monitoring_pc()

# Jika belum login
else:
    # Header untuk halaman login
    st.title("👋 Selamat Datang")
    st.subheader("Sistem Manajemen Praktik & Guru")
    st.caption("Silakan login untuk mengakses sistem")
    
    st.divider()
    
    # Login options dengan layout yang lebih baik
    st.subheader("Pilih menu:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔐 Login", use_container_width=True, type="primary"):
            st.session_state.page = "login"
    
    with col2:
        if st.button("📝 Register", use_container_width=True):
            st.session_state.page = "register"
    
    with col3:
        if st.button("🔁 Lupa Password", use_container_width=True):
            st.session_state.page = "forgot"

    st.divider()

    # Show appropriate page
    if st.session_state.page == "login":
        show_login()
    elif st.session_state.page == "register":
        show_register()
    elif st.session_state.page == "forgot":
        show_forgot_password()