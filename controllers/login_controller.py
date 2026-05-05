from services.auth_service import login

class LoginController:
    def __init__(self, view):
        self.view = view

    def handle_login(self, username, password):
        usuario = login(username, password)
        if usuario:
            self.view.show_message("Éxito", "Acceso correcto, cargando...")
            # Usar after() para abrir el dashboard FUERA del callback de Tkinter
            self.view.after(300, lambda: self._abrir_dashboard())
        else:
            self.view.show_error("Error", "Usuario o contraseña incorrectos.")

    def _abrir_dashboard(self):
        # Importación local para evitar importaciones circulares
        from views.dashboard_view import DashboardView

        # Ocultar la ventana de login y abrir el dashboard
        self.view.withdraw()
        dashboard = DashboardView()
        dashboard.protocol("WM_DELETE_WINDOW", lambda: self._on_close(dashboard))
        dashboard.mainloop()

    def _on_close(self, dashboard):
        """Cierra el dashboard y la ventana de login por completo."""
        dashboard.destroy()
        self.view.destroy()
