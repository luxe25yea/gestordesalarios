import customtkinter as ctk
from controllers.empleado_controller import EmpleadoController

# ── Paleta de colores ────────────────────────────────────────────────────────
BG_DARK   = "#0f1117"
CARD_BG   = "#1e2535"
EDIT_BG   = "#1a2540"
BORDER    = "#334155"
ACCENT    = "#38bdf8"
TEXT_1    = "#f1f5f9"
TEXT_2    = "#94a3b8"
TEXT_3    = "#64748b"
RED_ERR   = "#f87171"
GREEN     = "#4ade80"
ORANGE    = "#fb923c"


class EmpleadosView(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_DARK,
                         scrollbar_button_color=BORDER, **kwargs)
        self.controller = EmpleadoController(self)
        self._edit_panel = None   # referencia al panel de edición activo
        self._editing_id = None   # id del empleado en edición
        self._build_ui()

    # ══════════════════════════════════════════════════════════════════════════
    #  UI Principal
    # ══════════════════════════════════════════════════════════════════════════
    def _build_ui(self):
        # ── Encabezado ────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(28, 20))

        ctk.CTkLabel(
            header,
            text="👥  Gestión de Empleados",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=TEXT_1
        ).pack(side="left")

        ctk.CTkButton(
            header, text="🔄  Actualizar", width=120, height=55,
            corner_radius=8, fg_color="#263046", hover_color=CARD_BG,
            text_color=ACCENT, font=ctk.CTkFont("Segoe UI", 12),
            command=self.controller.load_employees
        ).pack(side="right")

        # ── Tarjeta: Agregar empleado ──────────────────────────────────────────
        self._build_add_card()

        # ── Panel de edición (oculto inicialmente) ────────────────────────────
        self._edit_panel_slot = ctk.CTkFrame(self, fg_color="transparent")
        self._edit_panel_slot.pack(fill="x", padx=30)

        # ── Tarjeta: Tabla de empleados ───────────────────────────────────────
        self._build_table_card()

        # Carga inicial
        self.controller.load_employees()

    # ── Tarjeta «Agregar» ─────────────────────────────────────────────────────
    def _build_add_card(self):
        card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                            border_width=1, border_color=BORDER)
        card.pack(fill="x", padx=30, pady=(0, 16))

        ctk.CTkLabel(
            card, text="➕  Agregar Nuevo Empleado",
            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=TEXT_1
        ).pack(anchor="w", padx=22, pady=(16, 4))

        ctk.CTkLabel(
            card, text="Completa los campos y presiona «Agregar».",
            font=ctk.CTkFont("Segoe UI", 11), text_color=TEXT_3
        ).pack(anchor="w", padx=22, pady=(0, 12))

        fields = ctk.CTkFrame(card, fg_color="transparent")
        fields.pack(fill="x", padx=22, pady=(0, 8))
        fields.columnconfigure((0, 1, 2, 3), weight=1)

        self.entry_nombre  = self._labeled_entry(fields, 0, "Nombre completo", "Ej: Juan García")
        self.entry_puesto  = self._labeled_entry(fields, 1, "Puesto / Cargo",  "Ej: Operador")
        self.entry_salario = self._labeled_entry(fields, 2, "Salario Diario",  "Ej: 350.00")

        ctk.CTkButton(
            fields, text="+ Agregar", height=38, corner_radius=8,
            fg_color="#0ea5e9", hover_color="#0284c7",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 12, "bold"),
            command=self._on_add
        ).grid(row=1, column=3, padx=(12, 0), sticky="ew")

        self.lbl_status = ctk.CTkLabel(
            card, text="", font=ctk.CTkFont("Segoe UI", 11)
        )
        self.lbl_status.pack(anchor="w", padx=22, pady=(0, 14))

    # ── Tarjeta «Tabla» ───────────────────────────────────────────────────────
    def _build_table_card(self):
        self.table_card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                                       border_width=1, border_color=BORDER)
        self.table_card.pack(fill="both", padx=30, pady=(0, 28), expand=True)

        ctk.CTkLabel(
            self.table_card, text="Empleados Registrados",
            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=TEXT_1
        ).pack(anchor="w", padx=22, pady=(16, 10))

        # Cabecera
        hdr = ctk.CTkFrame(self.table_card, fg_color="#263046", corner_radius=8)
        hdr.pack(fill="x", padx=16, pady=(0, 4))

        for title, w in [("ID", 50), ("Nombre", 200), ("Puesto", 160),
                         ("Salario/Día", 130), ("Acciones", 180)]:
            ctk.CTkLabel(
                hdr, text=title, width=w, anchor="w",
                font=ctk.CTkFont("Segoe UI", 11, "bold"), text_color=ACCENT
            ).pack(side="left", padx=10, pady=9)

        # Cuerpo de filas (se regenera en cada populate_table)
        self.table_body = ctk.CTkFrame(self.table_card, fg_color="transparent")
        self.table_body.pack(fill="both", padx=16, pady=(0, 14), expand=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  Populate (READ)
    # ══════════════════════════════════════════════════════════════════════════
    def populate_table(self, empleados):
        # Limpiar filas anteriores
        for w in self.table_body.winfo_children():
            w.destroy()

        if not empleados:
            ctk.CTkLabel(
                self.table_body,
                text="No hay empleados registrados.",
                font=ctk.CTkFont("Segoe UI", 12), text_color=TEXT_3
            ).pack(pady=18)
            return

        for i, emp in enumerate(empleados):
            row_color = "#1a2030" if i % 2 else CARD_BG
            row = ctk.CTkFrame(self.table_body, fg_color=row_color, corner_radius=6)
            row.pack(fill="x", pady=2)

            # Datos
            for val, w in [(str(emp.id), 50), (emp.nombre, 200),
                           (emp.puesto, 160), (f"${emp.salario_diario:,.2f}", 130)]:
                ctk.CTkLabel(
                    row, text=val, width=w, anchor="w",
                    font=ctk.CTkFont("Segoe UI", 12), text_color=TEXT_2
                ).pack(side="left", padx=10, pady=8)

            # ── Botones de acción ─────────────────────────────────────────────
            actions = ctk.CTkFrame(row, fg_color="transparent", width=180)
            actions.pack(side="left", padx=6, pady=4)

            ctk.CTkButton(
                actions, text="✏ Editar", width=82, height=30,
                corner_radius=6, fg_color="#1d4ed8", hover_color="#1e40af",
                text_color="#fff", font=ctk.CTkFont("Segoe UI", 11),
                command=lambda e=emp: self._open_edit_panel(e)
            ).pack(side="left", padx=(0, 6))

            ctk.CTkButton(
                actions, text="🗑 Eliminar", width=88, height=30,
                corner_radius=6, fg_color="#991b1b", hover_color="#7f1d1d",
                text_color="#fff", font=ctk.CTkFont("Segoe UI", 11),
                command=lambda e=emp: self._confirm_delete(e)
            ).pack(side="left")

    # ══════════════════════════════════════════════════════════════════════════
    #  Panel de edición (UPDATE)
    # ══════════════════════════════════════════════════════════════════════════
    def _open_edit_panel(self, emp):
        """Abre (o reemplaza) el panel de edición debajo del formulario de alta."""
        self.close_edit_panel()   # Cerrar si había uno abierto
        self._editing_id = emp.id

        panel = ctk.CTkFrame(
            self._edit_panel_slot,
            corner_radius=14, fg_color=EDIT_BG,
            border_width=2, border_color=ACCENT
        )
        panel.pack(fill="x", pady=(0, 16))
        self._edit_panel = panel

        # Encabezado del panel
        top = ctk.CTkFrame(panel, fg_color="transparent")
        top.pack(fill="x", padx=22, pady=(16, 4))

        ctk.CTkLabel(
            top, text=f"✏  Editando empleado #{emp.id}",
            font=ctk.CTkFont("Segoe UI", 14, "bold"), text_color=ACCENT
        ).pack(side="left")

        ctk.CTkButton(
            top, text="✕ Cancelar", width=90, height=30,
            corner_radius=6, fg_color="#334155", hover_color="#475569",
            text_color=TEXT_2, font=ctk.CTkFont("Segoe UI", 11),
            command=self.close_edit_panel
        ).pack(side="right")

        # Campos de edición
        fields = ctk.CTkFrame(panel, fg_color="transparent")
        fields.pack(fill="x", padx=22, pady=(8, 6))
        fields.columnconfigure((0, 1, 2, 3), weight=1)

        self.edit_nombre  = self._labeled_entry(fields, 0, "Nombre completo", emp.nombre)
        self.edit_puesto  = self._labeled_entry(fields, 1, "Puesto / Cargo",  emp.puesto)
        self.edit_salario = self._labeled_entry(fields, 2, "Salario Diario",  str(emp.salario_diario))

        # Pre-rellenar con datos actuales
        self.edit_nombre.insert(0, emp.nombre)
        self.edit_puesto.insert(0, emp.puesto)
        self.edit_salario.insert(0, str(emp.salario_diario))

        ctk.CTkButton(
            fields, text="💾 Guardar", height=38, corner_radius=8,
            fg_color="#16a34a", hover_color="#15803d",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 12, "bold"),
            command=self._on_update
        ).grid(row=1, column=3, padx=(12, 0), sticky="ew")

        ctk.CTkFrame(panel, height=1, fg_color=BORDER).pack(
            fill="x", padx=22, pady=(8, 14)
        )

    def close_edit_panel(self):
        """Cierra el panel de edición si está abierto."""
        if self._edit_panel and self._edit_panel.winfo_exists():
            self._edit_panel.destroy()
        self._edit_panel = None
        self._editing_id = None

    # ══════════════════════════════════════════════════════════════════════════
    #  Diálogo de confirmación (DELETE)
    # ══════════════════════════════════════════════════════════════════════════
    def _confirm_delete(self, emp):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar eliminación")
        dialog.geometry("380x200")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#1e2535")
        dialog.grab_set()   # Modal

        ctk.CTkLabel(
            dialog,
            text="⚠  ¿Eliminar empleado?",
            font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color="#fbbf24"
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            dialog,
            text=f"Se eliminará a «{emp.nombre}» de forma permanente.\nEsta acción no se puede deshacer.",
            font=ctk.CTkFont("Segoe UI", 12), text_color=TEXT_2,
            justify="center"
        ).pack(pady=(0, 20))

        btn_row = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_row.pack()

        ctk.CTkButton(
            btn_row, text="Cancelar", width=120, height=36,
            corner_radius=8, fg_color="#334155", hover_color="#475569",
            text_color=TEXT_2, font=ctk.CTkFont("Segoe UI", 12),
            command=dialog.destroy
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row, text="🗑 Eliminar", width=120, height=36,
            corner_radius=8, fg_color="#dc2626", hover_color="#b91c1c",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 12, "bold"),
            command=lambda: (dialog.destroy(),
                             self.controller.delete_employee(emp.id, emp.nombre))
        ).pack(side="left", padx=8)

    # ══════════════════════════════════════════════════════════════════════════
    #  Eventos internos
    # ══════════════════════════════════════════════════════════════════════════
    def _on_add(self):
        self.controller.add_employee(
            self.entry_nombre.get().strip(),
            self.entry_puesto.get().strip(),
            self.entry_salario.get().strip()
        )
        self.entry_nombre.delete(0, "end")
        self.entry_puesto.delete(0, "end")
        self.entry_salario.delete(0, "end")

    def _on_update(self):
        self.controller.update_employee(
            self._editing_id,
            self.edit_nombre.get().strip(),
            self.edit_puesto.get().strip(),
            self.edit_salario.get().strip()
        )

    # ══════════════════════════════════════════════════════════════════════════
    #  Mensajes de estado
    # ══════════════════════════════════════════════════════════════════════════
    def show_message(self, title, message):
        self.lbl_status.configure(text=f"✓  {message}", text_color=GREEN)

    def show_error(self, title, message):
        self.lbl_status.configure(text=f"⚠  {message}", text_color=RED_ERR)

    # ══════════════════════════════════════════════════════════════════════════
    #  Utilidad: entrada con etiqueta
    # ══════════════════════════════════════════════════════════════════════════
    def _labeled_entry(self, parent, col, label, placeholder):
        pad = (0 if col == 0 else 12, 0)
        ctk.CTkLabel(
            parent, text=label,
            font=ctk.CTkFont("Segoe UI", 11), text_color=TEXT_3
        ).grid(row=0, column=col, sticky="w", padx=pad, pady=(0, 4))

        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            height=38, corner_radius=8,
            border_color=BORDER, fg_color="#0f1117",
            text_color=TEXT_1, font=ctk.CTkFont("Segoe UI", 12)
        )
        entry.grid(row=1, column=col, sticky="ew", padx=pad)
        return entry
