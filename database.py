import sqlite3
import random

DB = "logs.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Tabela de usuários
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            access_code TEXT
        )
    """)

    # Tabela de admins
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Cria admin inicial se não existir
    c.execute("SELECT * FROM admin")
    if c.fetchone() is None:
        c.execute("INSERT INTO admin (nome, senha) VALUES ('admin', '1234')")

    conn.commit()
    conn.close()


# -------------------- USUÁRIOS --------------------
def create_user(nome, senha):
    """Cria um usuário com código de acesso aleatório"""
    code = str(random.randint(1000, 9999))

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (nome, senha, access_code) VALUES (?, ?, ?)",
        (nome, senha, code)
    )
    conn.commit()
    conn.close()

    return code

def get_user_by_code(code):
    """Busca usuário pelo código de acesso"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT nome FROM users WHERE access_code = ?", (code,))
    row = c.fetchone()
    conn.close()
    return row

def get_user_by_name(nome):
    """Busca usuário pelo nome"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT senha FROM users WHERE nome = ?", (nome,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


# -------------------- ADMIN -----------------------
def get_admin_password_by_name(nome):
    """Busca senha do admin pelo nome"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT senha FROM admin WHERE nome = ?", (nome,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def create_admin(nome, senha):
    """Cria um novo admin"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO admin (nome, senha) VALUES (?, ?)", (nome, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Nome já existe


# -------------------- INICIALIZA BANCO -----------------------
if __name__ == "__main__":
    init_db()
    print("Banco inicializado com sucesso!")
