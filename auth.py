from database import get_user_by_code, get_admin_password_by_name, create_user as db_create_user, create_admin as db_create_admin

# -------------------- USUÁRIOS --------------------
def validar_codigo(codigo):
    """Valida o código de acesso do usuário"""
    return get_user_by_code(codigo)

def criar_usuario(nome, senha):
    """Cria um novo usuário e retorna o código de acesso"""
    return db_create_user(nome, senha)

# -------------------- ADMIN -----------------------
def validar_admin(nome, senha):
    """Valida login do admin pelo nome e senha"""
    senha_correta = get_admin_password_by_name(nome)
    if senha_correta is None:
        return False
    return senha == senha_correta

def criar_admin(nome, senha):
    """Cria um novo admin e retorna True se sucesso"""
    return db_create_admin(nome, senha)
