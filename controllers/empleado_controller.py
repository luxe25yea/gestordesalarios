from services.empleado_service import (
    create_employee, get_all_employees,
    update_employee, delete_employee
)

class EmpleadoController:
    def __init__(self, view):
        self.view = view

    # ── Leer ─────────────────────────────────────────────────────────────────
    def load_employees(self):
        empleados = get_all_employees()
        self.view.populate_table(empleados)

    # ── Crear ─────────────────────────────────────────────────────────────────
    def add_employee(self, nombre, puesto, salario_diario):
        if not nombre or not puesto or not salario_diario:
            self.view.show_error("Error", "Todos los campos son obligatorios.")
            return
        try:
            salario = float(salario_diario)
            create_employee(nombre, puesto, salario)
            self.load_employees()
            self.view.show_message("Éxito", f"Empleado «{nombre}» agregado correctamente.")
        except ValueError:
            self.view.show_error("Error", "El salario debe ser un número válido.")

    # ── Actualizar ────────────────────────────────────────────────────────────
    def update_employee(self, emp_id, nombre, puesto, salario_diario):
        if not nombre or not puesto or not salario_diario:
            self.view.show_error("Error", "Todos los campos son obligatorios.")
            return
        try:
            salario = float(salario_diario)
            update_employee(emp_id, nombre, puesto, salario)
            self.load_employees()
            self.view.show_message("Éxito", f"Empleado #{emp_id} actualizado correctamente.")
            self.view.close_edit_panel()
        except ValueError:
            self.view.show_error("Error", "El salario debe ser un número válido.")

    # ── Eliminar ──────────────────────────────────────────────────────────────
    def delete_employee(self, emp_id, nombre):
        delete_employee(emp_id)
        self.load_employees()
        self.view.show_message("Éxito", f"Empleado «{nombre}» eliminado.")
