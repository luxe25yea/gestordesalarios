import matplotlib.pyplot as plt

def generate_salary_chart(data, output_path="temp_chart.png"):
    """Genera un gráfico de barras con el salario de cada empleado y lo guarda como imagen."""
    if not data:
        return None
        
    nombres = [item['nombre'] for item in data]
    pagos = [item['total_pago'] for item in data]

    plt.figure(figsize=(8, 5))
    plt.bar(nombres, pagos, color='skyblue')
    plt.xlabel('Empleados')
    plt.ylabel('Salario Total ($)')
    plt.title('Salario Total por Empleado')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    return output_path
