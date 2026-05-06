"""
seed_data.py
Script para inicializar la base de datos e insertar datos de prueba.
Ejecutar UNA sola vez antes de iniciar la aplicación.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.init_db import initialize_database
from database.connection import get_connection
from utils.hash import hash_password

def seed():
    # 1. Crear tablas y usuario admin por defecto
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()

    # 2. Usuarios adicionales de prueba
    usuarios_extra = [
        ("supervisor", "super123"),
        ("recursos",   "rrhh2024"),
    ]
    for uname, pwd in usuarios_extra:
        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (uname,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
                (uname, hash_password(pwd))
            )

    # 3. Empleados de prueba
    empleados = [
        ("Carlos Ramírez",    "Operador de planta",  350.00),
        ("María López",       "Supervisora",          500.00),
        ("José Hernández",    "Técnico de campo",     420.00),
        ("Ana Martínez",      "Administrativa",       380.00),
        ("Luis Torres",       "Chofer",               310.00),
    ]
    for nombre, puesto, salario in empleados:
        cursor.execute(
            "INSERT INTO empleados (nombre, puesto, salario_diario) VALUES (?, ?, ?)",
            (nombre, puesto, salario)
        )

    conn.commit()

    # 4. Asistencias de prueba (IDs 1-5, semana pasada)
    from datetime import date, timedelta
    hoy = date.today()
    asistencias = [
        (1, str(hoy - timedelta(days=5)), 5),
        (2, str(hoy - timedelta(days=5)), 5),
        (3, str(hoy - timedelta(days=5)), 4),
        (4, str(hoy - timedelta(days=5)), 5),
        (5, str(hoy - timedelta(days=5)), 3),
        (1, str(hoy),                     3),
        (2, str(hoy),                     2),
    ]
    for emp_id, fecha, dias in asistencias:
        cursor.execute(
            "INSERT INTO asistencias (empleado_id, fecha, dias_trabajados) VALUES (?, ?, ?)",
            (emp_id, fecha, dias)
        )

    conn.commit()
    conn.close()

    print("✅ Base de datos inicializada con datos de prueba.")
    print("   Usuario por defecto: admin / admin123")
    print("   Empleados insertados:", len(empleados))

if __name__ == "__main__":
    seed()
