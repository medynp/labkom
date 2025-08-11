# 🧪 Sistem Manajemen Lab (Lab Management System)

A comprehensive web-based laboratory management system built with Streamlit for educational institutions to manage teachers, laboratories, equipment, and lab usage efficiently.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔐 Authentication & Authorization
- User registration and login system
- Password reset functionality
- Token-based session management
- Role-based access control

### 👨‍🏫 Teacher Management
- Add, edit, and delete teacher records
- Teacher profile management
- Search and filter functionality

### 🧪 Laboratory Management
- Laboratory registration and management
- Lab capacity and equipment tracking
- Lab status monitoring

### 📦 Equipment Management
- Equipment inventory tracking
- Equipment categorization
- Condition monitoring (Baik, Rusak Ringan, Rusak Berat, Dalam Perbaikan)
- Status management
- Lab assignment for equipment

### 🔧 Maintenance Management
- Equipment maintenance scheduling
- Maintenance history tracking
- Maintenance status updates

### 📊 Lab Usage Management
- Lab booking and scheduling
- Usage history and reports
- Real-time lab availability

### 📈 Dashboard & Analytics
- Overview metrics and statistics
- Quick action buttons
- System status monitoring

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Authentication**: Custom token-based system
- **UI Components**: Streamlit native components
- **Data Handling**: Pandas

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step-by-step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lab-management-system.git
   cd lab-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python setup_database.py
   ```

5. **Run the application**
   ```bash
   streamlit run labkom/app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:8501`

## 📖 Usage

### First Time Setup

1. **Register an Admin Account**
   - Navigate to the registration page
   - Create your admin account
   - Login with your credentials

2. **Set Up Laboratories**
   - Go to "Manajemen Lab"
   - Add your laboratory rooms
   - Configure capacity and details

3. **Add Teachers**
   - Navigate to "Manajemen Guru"
   - Add teacher profiles
   - Assign roles and permissions

4. **Manage Equipment**
   - Go to "Manajemen Barang"
   - Add equipment inventory
   - Assign equipment to laboratories
   - Set categories and conditions

### Daily Operations

- **Monitor Dashboard**: Check system overview and quick stats
- **Schedule Lab Usage**: Book laboratories for classes
- **Track Equipment**: Monitor equipment status and maintenance
- **Generate Reports**: View usage statistics and reports

## 📁 Project Structure

```
labkom/
├── app.py                      # Main application entry point
├── views/                      # UI view components
│   ├── login.py               # Login page
│   ├── register.py            # Registration page
│   ├── forgot_password.py     # Password reset
│   ├── guru.py                # Teacher management
│   ├── lab.py                 # Laboratory management
│   ├── barang.py              # Equipment management
│   ├── edit_barang.py         # Equipment editing
│   ├── maintenance.py         # Maintenance management
│   ├── penggunaan_lab.py      # Lab usage tracking
│   └── edit_penggunaan_lab.py # Lab usage editing
├── utils/                      # Utility modules
│   ├── database.py            # Database connection
│   ├── session.py             # Session management
│   └── token_db.py            # Token validation
└── requirements.txt           # Python dependencies
```

## 🗄 Database Schema

### Main Tables

#### Users
- `id` (Primary Key)
- `username`
- `email`
- `password_hash`
- `role`
- `created_at`

#### Lab
- `id` (Primary Key)
- `nama_lab`
- `kapasitas`
- `lokasi`
- `status`

#### Barang (Equipment)
- `id` (Primary Key)
- `nama_barang`
- `jumlah`
- `kondisi` (Baik, Rusak Ringan, Rusak Berat, Dalam Perbaikan)
- `status`
- `lab_id` (Foreign Key)
- `kategori`

#### Guru (Teachers)
- `id` (Primary Key)
- `nama`
- `email`
- `mata_pelajaran`
- `status`

#### Maintenance
- `id` (Primary Key)
- `barang_id` (Foreign Key)
- `tanggal_maintenance`
- `deskripsi`
- `status`
