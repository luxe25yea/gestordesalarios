import customtkinter as ctk
from views.empleados_view import EmpleadosView
from views.jornadas_view import JornadasView
from views.reportes_view import ReportesView
from views.settings_view import SettingsView
from services.empleado_service import get_all_employees
from services.nomina_service import get_report_data
import os
from PIL import Image

# ─── Colores del tema ────────────────────────────────────────────────────────
BG_DARK   = "#0f1117"
SIDEBAR   = "#1a1f2e"
CARD_BG   = "#1e2535"
BORDER    = "#334155"
ACCENT    = "#38bdf8"
TEXT_1    = "#f1f5f9"
TEXT_2    = "#94a3b8"
TEXT_3    = "#64748b"
GREEN     = "#4ade80"
ORANGE    = "#fb923c"
PURPLE    = "#a78bfa"

def make_card(parent, title, value, icon, color):
    """Crea una tarjeta de resumen estilo KPI."""
    card = ctk.CTkFrame(parent, corner_radius=14, fg_color=CARD_BG,
                        border_width=1, border_color=BORDER)

    top = ctk.CTkFrame(card, fg_color="transparent")
    top.pack(fill="x", padx=16, pady=(16, 8))

    ctk.CTkLabel(top, text=icon, font=("Segoe UI Emoji", 22)).pack(side="left")

    ctk.CTkLabel(
        top, text=title,
        font=ctk.CTkFont("Segoe UI", 11),
        text_color=TEXT_3
    ).pack(side="left", padx=(8, 0))

    ctk.CTkLabel(
        card, text=value,
        font=ctk.CTkFont("Segoe UI", 26, "bold"),
        text_color=color
    ).pack(padx=16, anchor="w")

    ctk.CTkFrame(card, height=3, corner_radius=2, fg_color=color).pack(
        fill="x", padx=16, pady=(8, 14)
    )
    return card


class DashboardView(ctk.CTk):
    def __init__(self, current_username="admin"):
        super().__init__()
        self.current_username = current_username
        self.title("Aguas Moya - Panel de Control")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(fg_color=BG_DARK)

        self._active_btn = None
        self.frames = {}

        self._build_layout()
        self.show_section("inicio")

    # ── Layout principal ─────────────────────────────────────────────────────
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

    # ── Sidebar ──────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=SIDEBAR)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Branding
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(24, 8))
        
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "LogoMoyaMejorado.png")
        try:
            self.dashboard_logo = ctk.CTkImage(light_image=Image.open(logo_path), dark_image=Image.open(logo_path), size=(45, 45))
            ctk.CTkLabel(brand, text="", image=self.dashboard_logo).pack(side="left")
        except Exception as e:
            print("Error loading dashboard logo:", e)
           

        ctk.CTkLabel(
            brand, text="Aguas Moya",
            font=ctk.CTkFont("Segoe UI", 16, "bold"),
            text_color=ACCENT
        ).pack(side="left", padx=8)

        # Separador
        ctk.CTkFrame(sidebar, height=1, fg_color=BORDER).pack(
            fill="x", padx=16, pady=(8, 20)
        )

        # Menú de navegación
        nav_items = [
            ("inicio",     "🏠",  "Inicio"),
            ("empleados",  "👥",  "Empleados"),
            ("jornadas",   "📅",  "Jornadas"),
            ("reportes",   "📊",  "Reportes"),
            ("configuracion", "⚙️", "Configuración"),
        ]

        self._nav_buttons = {}
        for key, icon, label in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"  {icon}  {label}",
                anchor="w",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#263046",
                text_color=TEXT_2,
                font=ctk.CTkFont("Segoe UI", 13),
                command=lambda k=key: self.show_section(k)
            )
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_buttons[key] = btn

        # Versión
        ctk.CTkLabel(
            sidebar, text="v1.0.0  •  Aguas Moya",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TEXT_3
        ).pack(side="bottom", pady=16)

    # ── Área de contenido ─────────────────────────────────────────────────────
    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_DARK)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.frames["inicio"]    = self._build_home()
        self.frames["empleados"] = EmpleadosView(self.content)
        self.frames["jornadas"]  = JornadasView(self.content)
        self.frames["reportes"]  = ReportesView(self.content)
        self.frames["configuracion"] = SettingsView(self.content, current_username=self.current_username)

    # ── Vista de Inicio ───────────────────────────────────────────────────────
    def _build_home(self):
        frame = ctk.CTkScrollableFrame(self.content, fg_color=BG_DARK, scrollbar_button_color=BORDER)

        # Header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(28, 24))

        ctk.CTkLabel(
            header,
            text="Panel de Control",
            font=ctk.CTkFont("Segoe UI", 26, "bold"),
            text_color=TEXT_1
        ).pack(side="left")

        # ── Tarjetas KPI ──────────────────────────────────────────────────────
        try:
            empleados = get_all_employees()
            num_emp = len(empleados)
        except Exception:
            num_emp = 0

        try:
            data = get_report_data()
            total_nomina = sum(d["total_pago"] for d in data)
            num_reportes = len(data)
        except Exception:
            total_nomina = 0.0
            num_reportes = 0

        cards_data = [
            ("Total Empleados",  str(num_emp),              "👥", ACCENT),
            ("Nómina Total",     f"${total_nomina:,.2f}",   "💰", GREEN),
            ("Registros",        str(num_reportes),          "📋", ORANGE),
            ("Estado",           "Activo",                   "✅", PURPLE),
        ]

        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="x", padx=30, pady=(0, 24))
        grid.columnconfigure((0, 1, 2, 3), weight=1)

        for col, (title, value, icon, color) in enumerate(cards_data):
            card = make_card(grid, title, value, icon, color)
            card.grid(row=0, column=col, padx=8, pady=4, sticky="nsew")

        # ── Resumen de empleados ──────────────────────────────────────────────
        sec = ctk.CTkFrame(frame, fg_color="transparent")
        sec.pack(fill="x", padx=30, pady=(0, 24))

        ctk.CTkLabel(
            sec,
            text="Empleados Registrados",
            font=ctk.CTkFont("Segoe UI", 16, "bold"),
            text_color=TEXT_1
        ).pack(anchor="w", pady=(0, 10))

        table_frame = ctk.CTkFrame(sec, corner_radius=12, fg_color=CARD_BG,
                                   border_width=1, border_color=BORDER)
        table_frame.pack(fill="x")

        # Cabecera de tabla
        hdr = ctk.CTkFrame(table_frame, fg_color="#263046", corner_radius=0)
        hdr.pack(fill="x")
        for col_text, w in [("ID", 60), ("Nombre", 220), ("Puesto", 180), ("Salario Diario", 140)]:
            ctk.CTkLabel(
                hdr, text=col_text, width=w,
                font=ctk.CTkFont("Segoe UI", 12, "bold"),
                text_color=ACCENT, anchor="w"
            ).pack(side="left", padx=14, pady=10)

        try:
            empleados = get_all_employees()
        except Exception:
            empleados = []

        if empleados:
            for i, emp in enumerate(empleados[:10]):
                row_color = CARD_BG if i % 2 == 0 else "#1a2030"
                row = ctk.CTkFrame(table_frame, fg_color=row_color, corner_radius=0)
                row.pack(fill="x")
                for val, w in [(str(emp.id), 60), (emp.nombre, 220), (emp.puesto, 180),
                               (f"${emp.salario_diario:,.2f}", 140)]:
                    ctk.CTkLabel(
                        row, text=val, width=w,
                        font=ctk.CTkFont("Segoe UI", 12),
                        text_color=TEXT_2, anchor="w"
                    ).pack(side="left", padx=14, pady=9)
        else:
            ctk.CTkLabel(
                table_frame,
                text="Sin empleados registrados aún.",
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=TEXT_3
            ).pack(pady=20)

        return frame

    # ── Navegación ────────────────────────────────────────────────────────────
    def show_section(self, name):
        # Limpiar selección anterior
        if self._active_btn:
            self._active_btn.configure(fg_color="transparent", text_color=TEXT_2)

        btn = self._nav_buttons[name]
        btn.configure(fg_color="#263046", text_color=ACCENT)
        self._active_btn = btn

        # Ocultar todos los frames
        for key, frame in self.frames.items():
            frame.grid_forget()

        # Si vamos al inicio, reconstruir para datos frescos
        if name == "inicio":
            self.frames["inicio"].destroy()
            self.frames["inicio"] = self._build_home()
        elif hasattr(self.frames[name], 'refresh'):
            self.frames[name].refresh()
        elif name == "empleados" and hasattr(self.frames[name], 'controller') and hasattr(self.frames[name].controller, 'load_employees'):
            self.frames[name].controller.load_employees()

        self.frames[name].grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
