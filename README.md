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

## 🖼 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Equipment Management
![Equipment Management](screenshots/equipment.png)

### Lab Management
![Lab Management](screenshots/lab.png)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📝 Requirements

```txt
streamlit>=1.28.0
pandas>=1.5.0
sqlite3
datetime
hashlib
secrets
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
DATABASE_PATH=./database.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Database Configuration
The system uses SQLite by default. To use a different database:

1. Update `utils/database.py`
2. Install appropriate database drivers
3. Update connection strings

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure database file exists
   - Check file permissions
   - Run database setup script

2. **Streamlit Port Already in Use**
   ```bash
   streamlit run labkom/app.py --server.port 8502
   ```

3. **Module Import Errors**
   - Verify virtual environment is activated
   - Install missing dependencies
   - Check Python path

## 📊 System Requirements

- **Minimum**: Python 3.7, 2GB RAM, 1GB storage
- **Recommended**: Python 3.9+, 4GB RAM, 2GB storage
- **Browser**: Chrome, Firefox, Safari (latest versions)

## 🔒 Security Features

- Password hashing with secure algorithms
- Token-based authentication
- Session management
- Input validation and sanitization
- SQL injection prevention

## 📈 Future Enhancements

- [ ] Email notifications
- [ ] Advanced reporting and analytics
- [ ] Mobile responsive design
- [ ] API integration
- [ ] Backup and restore functionality
- [ ] Multi-language support
- [ ] Advanced user roles and permissions

## 📞 Support

For support and questions:

- **Issues**: [GitHub Issues](https://github.com/yourusername/lab-management-system/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/lab-management-system/wiki)
- **Email**: support@yourdomain.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Contributors and testers
- Educational institutions for requirements and feedback

---

**Made with ❤️ for educational institutions**

*Last updated: December 2024*
```

I've also created a requirements.txt file for the dependencies:

```txt:requirements.txt
streamlit>=1.28.0
pandas>=1.5.0
python-dateutil>=2.8.0
```

And here's a simple setup script for the database:

```python:setup_database.py
import sqlite3
import os
from datetime import datetime

def setup_database():
    """Initialize the database with required tables"""
    
    # Create database directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create lab table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_lab TEXT NOT NULL,
            kapasitas INTEGER,
            lokasi TEXT,
            status TEXT DEFAULT 'aktif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create barang table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_barang TEXT NOT NULL,
            jumlah INTEGER DEFAULT 1,
            kondisi TEXT DEFAULT 'Baik',
            status TEXT DEFAULT 'aktif',
            lab_id INTEGER,
            kategori TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lab_id) REFERENCES lab (id)
        )
    ''')
    
    # Create guru table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guru (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT UNIQUE,
            mata_pelajaran TEXT,
            status TEXT DEFAULT 'aktif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create maintenance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barang_id INTEGER,
            tanggal_maintenance DATE,
            deskripsi TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (barang_id) REFERENCES barang (id)
        )
    ''')
    
    # Create penggunaan_lab table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS penggunaan_lab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER,
            guru_id INTEGER,
            tanggal_penggunaan DATE,
            waktu_mulai TIME,
            waktu_selesai TIME,
            mata_pelajaran TEXT,
            jumlah_siswa INTEGER,
            keterangan TEXT,
            status TEXT DEFAULT 'aktif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lab_id) REFERENCES lab (id),
            FOREIGN KEY (guru_id) REFERENCES guru (id)
        )
    ''')
    
    # Create tokens table for session management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database setup completed successfully!")
    print("📁 Database location: data/database.db")

if __name__ == "__main__":
    setup_database()
