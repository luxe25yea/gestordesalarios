import customtkinter as ctk
from controllers.login_controller import LoginController
import os
from PIL import Image

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aguas Moya-Sistema de Gestión Salarial")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(fg_color="#0f1117")

        self.controller = LoginController(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._build_ui()

    def _build_ui(self):
        # ── Panel izquierdo (branding) ──────────────────────────────────────
        left = ctk.CTkFrame(self, width=400, corner_radius=0, fg_color="#1a1f2e")
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "LogoMoyaMejorado.png")
        try:
            self.logo_img = ctk.CTkImage(light_image=Image.open(logo_path), dark_image=Image.open(logo_path), size=(150, 150))
            ctk.CTkLabel(left, text="", image=self.logo_img).pack(pady=(60, 0))
        except Exception as e:
            print("Error loading login logo:", e)
            ctk.CTkLabel(
                left, text="💧", font=("Segoe UI Emoji", 52)
            ).pack(pady=(100, 0))

        ctk.CTkLabel(
            left,
            text="Aguas Moya",
            font=ctk.CTkFont("Segoe UI", 30, "bold"),
            text_color="#274DF5"
        ).pack(pady=(8, 4))

        ctk.CTkLabel(
            left,
            text="Sistema de Gestión de\nJornadas y Salarios",
            font=ctk.CTkFont("Segoe UI", 15),
            text_color="#94a3b8",
            justify="center"
        ).pack()

        # Línea decorativa
        ctk.CTkFrame(left, height=2, width=200, fg_color="#38bdf8").pack(pady=30)

        ctk.CTkLabel(
            left,
            text="Reportes,Empleados\n Jornadas,Nómina",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color="#64748b",
            justify="center"
        ).pack()

        # ── Panel derecho (formulario) ───────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color="#0f1117")
        right.pack(side="right", fill="both", expand=True)

        # Contenedor centrador
        center = ctk.CTkFrame(right, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        card = ctk.CTkFrame(center, width=330, height=400,
                            corner_radius=16, fg_color="#1e2535",
                            border_width=1, border_color="#334155")
        card.pack()
        card.pack_propagate(False)  # Respetar width/height fijos

        ctk.CTkLabel(
            card,
            text="Iniciar Sesión",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color="#f1f5f9"
        ).pack(pady=(32, 4))

        ctk.CTkLabel(
            card,
            text="Ingresa tus credenciales para continuar",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color="#64748b"
        ).pack(pady=(0, 24))

        # Campo usuario
        ctk.CTkLabel(card, text="Usuario", font=ctk.CTkFont("Segoe UI", 12),
                     text_color="#94a3b8", anchor="w").pack(padx=28, fill="x")
        self.entry_username = ctk.CTkEntry(
            card,
            placeholder_text="Ej: admin",
            height=40,
            corner_radius=8,
            border_color="#334155",
            fg_color="#0f1117",
            text_color="#f1f5f9",
            font=ctk.CTkFont("Segoe UI", 13)
        )
        self.entry_username.pack(padx=28, pady=(4, 14), fill="x")

        # Campo contraseña
        ctk.CTkLabel(card, text="Contraseña", font=ctk.CTkFont("Segoe UI", 12),
                     text_color="#94a3b8", anchor="w").pack(padx=28, fill="x")
        pw_frame = ctk.CTkFrame(card, fg_color="transparent")
        pw_frame.pack(padx=28, pady=(4, 20), fill="x")
        pw_frame.columnconfigure(0, weight=1)

        self.entry_password = ctk.CTkEntry(
            pw_frame,
            placeholder_text="••••••••",
            show="•",
            height=40,
            corner_radius=8,
            border_color="#334155",
            fg_color="#0f1117",
            text_color="#f1f5f9",
            font=ctk.CTkFont("Segoe UI", 13)
        )
        self.entry_password.grid(row=0, column=0, sticky="ew")

        self.btn_toggle_pw = ctk.CTkButton(
            pw_frame, text="👁", width=40, height=40, corner_radius=8,
            fg_color="#1e2535", hover_color="#334155", border_color="#334155", border_width=1,
            text_color="#f1f5f9", font=ctk.CTkFont("Segoe UI", 16),
            command=self.toggle_password
        )
        self.btn_toggle_pw.grid(row=0, column=1, padx=(4, 0))

        # Botón
        self.btn_login = ctk.CTkButton(
            card,
            text="Ingresar al Sistema",
            height=42,
            corner_radius=8,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            fg_color="#0ea5e9",
            hover_color="#0284c7",
            command=self.on_login
        )
        self.btn_login.pack(padx=28, fill="x")

        # Mensaje de estado
        self.lbl_status = ctk.CTkLabel(
            card, text="", font=ctk.CTkFont("Segoe UI", 11), text_color="red"
        )
        self.lbl_status.pack(pady=(10, 0))

        # Enter para loguear
        self.bind("<Return>", lambda e: self.on_login())

    def on_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        self.controller.handle_login(username, password)

    def toggle_password(self):
        if self.entry_password.cget("show") == "•":
            self.entry_password.configure(show="")
            self.btn_toggle_pw.configure(text="🔒")
        else:
            self.entry_password.configure(show="•")
            self.btn_toggle_pw.configure(text="👁")

    def show_error(self, title, message):
        self.lbl_status.configure(text=f"⚠  {message}", text_color="#f87171")

    def show_message(self, title, message):
        self.lbl_status.configure(text=f"✓  {message}", text_color="#4ade80")

    def on_closing(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirmar salida", "¿Estás seguro que deseas salir de la aplicación?"):
            self.destroy()
