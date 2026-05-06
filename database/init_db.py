from database.connection import get_connection
from utils.hash import hash_password

def initialize_database():
    """Inicializa la base de datos creando tablas y cargando datos iniciales."""
    
    conn = get_connection()
    cursor = conn.cursor()

    # Activar claves foráneas en SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

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
    cursor.execute("SELECT 1 FROM usuarios WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = hash_password('admin123')
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
            ('admin', hashed_pw)
        )

    # Insertar empleados de prueba
    cursor.execute("SELECT COUNT(*) FROM empleados")
    if cursor.fetchone()[0] == 0:
        empleados_demo = [
            ("Juan Pérez", "Chofer", 300),
            ("Ana López", "Administración", 250),
            ("Carlos Ruiz", "Supervisor", 350)
        ]
        cursor.executemany(
            "INSERT INTO empleados (nombre, puesto, salario_diario) VALUES (?, ?, ?)",
            empleados_demo
        )

    conn.commit()
    conn.close()