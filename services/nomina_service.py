from database.connection import get_connection

def register_workday(empleado_id, fecha, dias_trabajados):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO asistencias (empleado_id, fecha, dias_trabajados) VALUES (?, ?, ?)",
                   (empleado_id, fecha, dias_trabajados))
    conn.commit()
    conn.close()

def get_report_data():
    """Obtiene datos generales para el reporte (todas las fechas)."""
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
        SELECT e.nombre, e.salario_diario, SUM(a.dias_trabajados) as total_dias
        FROM empleados e
        JOIN asistencias a ON e.id = a.empleado_id
        GROUP BY e.id
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    resultados = []
    for r in rows:
        total_pago = r['salario_diario'] * r['total_dias']
        resultados.append({
            'nombre': r['nombre'],
            'total_pago': total_pago
        })
    return resultados
