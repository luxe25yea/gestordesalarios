from database.connection import get_connection
from utils.hash import verify_password, hash_password
from models.usuario import Usuario

def login(username, password):
    """Autentica a un usuario y retorna un objeto Usuario si es válido."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row['password_hash']):
        return Usuario(row['id'], row['username'], row['password_hash'])
    return None

def update_credentials(old_username, new_username, new_password):
    """Actualiza el nombre de usuario y contraseña."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(new_password)
    cursor.execute("UPDATE usuarios SET username = ?, password_hash = ? WHERE username = ?", 
                   (new_username, hashed_pw, old_username))
    conn.commit()
    conn.close()
