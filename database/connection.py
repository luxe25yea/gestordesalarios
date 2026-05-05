import sqlite3
from config import DB_PATH

def get_connection():
    """Retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
    return conn
