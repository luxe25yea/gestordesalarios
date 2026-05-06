import customtkinter as ctk
from services.nomina_service import register_workday
from services.empleado_service import get_all_employees
from datetime import datetime
from tkcalendar import Calendar

BG_DARK = "#0f1117"
CARD_BG = "#1e2535"
BORDER  = "#334155"
ACCENT  = "#38bdf8"
TEXT_1  = "#f1f5f9"
TEXT_2  = "#94a3b8"
TEXT_3  = "#64748b"
RED_ERR = "#f87171"
GREEN   = "#4ade80"

class JornadasView(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_DARK, scrollbar_button_color=BORDER, **kwargs)
        self._build_ui()

    def _build_ui(self):
        # ── Encabezado ──────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(28, 20))

        ctk.CTkLabel(
            header,
            text="📅  Registro de Jornadas",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=TEXT_1
        ).pack(side="left")

        # ── Tarjeta de formulario ─────────────────────────────────────────────
        form_card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                                 border_width=1, border_color=BORDER)
        form_card.pack(fill="x", padx=30)

        ctk.CTkLabel(
            form_card,
            text="Nueva Jornada",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color=TEXT_1
        ).pack(anchor="w", padx=24, pady=(20, 4))

        ctk.CTkLabel(
            form_card,
            text="Completa los campos para registrar los días trabajados de un empleado.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_3
        ).pack(anchor="w", padx=24, pady=(0, 18))

        # Campos
        fields = ctk.CTkFrame(form_card, fg_color="transparent")
        fields.pack(fill="x", padx=24, pady=(0, 12))
        fields.columnconfigure((0, 1, 2), weight=1)

        def lbl(parent, col, text):
            ctk.CTkLabel(
                parent, text=text,
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=TEXT_3
            ).grid(row=0, column=col, sticky="w",
                   padx=(0 if col == 0 else 16, 0), pady=(0, 4))

        def entry(parent, col, placeholder):
            e = ctk.CTkEntry(
                parent, placeholder_text=placeholder,
                height=40, corner_radius=8,
                border_color=BORDER, fg_color="#0f1117",
                text_color=TEXT_1, font=ctk.CTkFont("Segoe UI", 12)
            )
            e.grid(row=1, column=col, sticky="ew",
                   padx=(0 if col == 0 else 16, 0))
            return e

        lbl(fields, 0, "ID del Empleado")
        lbl(fields, 1, "Días Trabajados")
        lbl(fields, 2, "Fecha (YYYY-MM-DD)")

        self.entry_emp_id = entry(fields, 0, "Ej: 1")
        self.entry_dias   = entry(fields, 1, "Ej: 5")

        date_frame = ctk.CTkFrame(fields, fg_color="transparent")
        date_frame.grid(row=1, column=2, sticky="ew", padx=(16, 0))
        date_frame.columnconfigure(0, weight=1)

        self.entry_fecha = ctk.CTkEntry(
            date_frame, placeholder_text=datetime.now().strftime("%Y-%m-%d"),
            height=40, corner_radius=8,
            border_color=BORDER, fg_color="#0f1117",
            text_color=TEXT_1, font=ctk.CTkFont("Segoe UI", 12)
        )
        self.entry_fecha.grid(row=0, column=0, sticky="ew")
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

        btn_cal = ctk.CTkButton(
            date_frame, text="📅", width=40, height=40,
            fg_color="#334155", hover_color="#475569", corner_radius=8,
            font=ctk.CTkFont("Segoe UI Emoji", 16),
            command=self.open_calendar
        )
        btn_cal.grid(row=0, column=1, padx=(4, 0))

        # Botón
        btn = ctk.CTkButton(
            form_card, text="✔  Registrar Jornada",
            height=42, corner_radius=8,
            fg_color="#0ea5e9", hover_color="#0284c7",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 13, "bold"),
            command=self.on_register
        )
        btn.pack(padx=24, pady=(8, 8), fill="x")

        self.lbl_status = ctk.CTkLabel(
            form_card, text="", font=ctk.CTkFont("Segoe UI", 11)
        )
        self.lbl_status.pack(padx=24, pady=(0, 16), anchor="w")

        # ── Tarjeta: Lista de empleados disponibles ───────────────────────────
        self.info_card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                                 border_width=1, border_color=BORDER)
        self.info_card.pack(fill="x", padx=30, pady=(20, 24))

        # Contenedor dinámico de empleados
        self.emp_list_frame = ctk.CTkFrame(self.info_card, fg_color="transparent")
        self.emp_list_frame.pack(fill="x")
        self.refresh()

    def refresh(self):
        for widget in self.emp_list_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.emp_list_frame,
            text="Empleados Disponibles",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            text_color=TEXT_1
        ).pack(anchor="w", padx=20, pady=(16, 8))

        try:
            empleados = get_all_employees()
        except Exception:
            empleados = []

        if empleados:
            for emp in empleados:
                row = ctk.CTkFrame(self.emp_list_frame, fg_color="#1a2030", corner_radius=8)
                row.pack(fill="x", padx=16, pady=3)
                ctk.CTkLabel(
                    row,
                    text=f"ID {emp.id}  •  {emp.nombre}  •  {emp.puesto}  •  ${emp.salario_diario:,.2f}/día",
                    font=ctk.CTkFont("Segoe UI", 12),
                    text_color=TEXT_2
                ).pack(padx=14, pady=8, anchor="w")
        else:
            ctk.CTkLabel(
                self.emp_list_frame,
                text="No hay empleados registrados.",
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=TEXT_3
            ).pack(padx=20, pady=12)

        ctk.CTkFrame(self.emp_list_frame, height=1, fg_color=BORDER).pack(
            fill="x", padx=16, pady=(8, 16)
        )

    def open_calendar(self):
        top = ctk.CTkToplevel(self)
        top.title("Seleccionar Fecha")
        top.geometry("300x250")
        top.attributes("-topmost", True)
        top.grab_set()

        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=20, padx=20, fill="both", expand=True)

        def set_date():
            self.entry_fecha.delete(0, "end")
            self.entry_fecha.insert(0, cal.get_date())
            top.destroy()

        ctk.CTkButton(top, text="Seleccionar", command=set_date).pack(pady=10)

    def on_register(self):
        try:
            emp_id = int(self.entry_emp_id.get())
            dias   = float(self.entry_dias.get())
            fecha  = self.entry_fecha.get().strip() or datetime.now().strftime("%Y-%m-%d")

            register_workday(emp_id, fecha, dias)
            self.lbl_status.configure(
                text=f"✓  Jornada de {dias} día(s) registrada para empleado #{emp_id}.",
                text_color=GREEN
            )
            self.entry_emp_id.delete(0, "end")
            self.entry_dias.delete(0, "end")
        except ValueError:
            self.lbl_status.configure(
                text="⚠  Error: Ingresa valores numéricos válidos.",
                text_color=RED_ERR
            )
