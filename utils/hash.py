import hashlib

def hash_password(password: str) -> str:
    """Genera un hash SHA-256 de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return hash_password(password) == hashed
