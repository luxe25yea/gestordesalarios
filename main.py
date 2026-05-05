import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from database.init_db import initialize_database
from views.login_view import LoginView

def main():
    # Configuración de CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Inicializar la base de datos (crea tablas y usuario admin si no existen)
    initialize_database()
    
    # Lanzar la aplicación desde el Login
    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    main()
