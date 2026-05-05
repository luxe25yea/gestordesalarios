from database.connection import get_connection
from utils.hash import hash_password

def initialize_database():
    """Crea las tablas necesarias e inserta el usuario por defecto."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Tabla de empleados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puesto TEXT NOT NULL,
            salario_diario REAL NOT NULL
        )
    ''')

    # Tabla de asistencias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            dias_trabajados REAL NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleados (id)
        )
    ''')

    # Insertar usuario admin si no existe
    cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = hash_password('admin123')
        cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", ('admin', hashed_pw))

    conn.commit()
    conn.close()
