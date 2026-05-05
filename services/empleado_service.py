from database.connection import get_connection
from models.empleado import Empleado

def create_employee(nombre, puesto, salario_diario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO empleados (nombre, puesto, salario_diario) VALUES (?, ?, ?)", 
                   (nombre, puesto, salario_diario))
    conn.commit()
    conn.close()

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados")
    rows = cursor.fetchall()
    conn.close()
    return [Empleado(r['id'], r['nombre'], r['puesto'], r['salario_diario']) for r in rows]

def update_employee(emp_id, nombre, puesto, salario_diario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE empleados SET nombre=?, puesto=?, salario_diario=? WHERE id=?", 
                   (nombre, puesto, salario_diario, emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
