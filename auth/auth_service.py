from utils.db import get_conn, hash_password

def login_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return cur.fetchone()

def register_user(username, email, password):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hash_password(password)))
        conn.commit()
        return "ok"
    except Exception as e:
        return str(e)

def reset_password(username, email, new_password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND email=?", (username, email))
    if cur.fetchone():
        cur.execute("UPDATE users SET password=? WHERE username=? AND email=?",
                    (hash_password(new_password), username, email))
        conn.commit()
        return "ok"
    else:
        return "Data tidak cocok"
