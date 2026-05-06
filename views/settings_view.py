import customtkinter as ctk
from services.auth_service import update_credentials

BG_DARK = "#0f1117"
CARD_BG = "#1e2535"
BORDER  = "#334155"
ACCENT  = "#38bdf8"
TEXT_1  = "#f1f5f9"
TEXT_2  = "#94a3b8"
TEXT_3  = "#64748b"
RED_ERR = "#f87171"
GREEN   = "#4ade80"

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, current_username="admin", **kwargs):
        super().__init__(master, fg_color=BG_DARK, **kwargs)
        self.current_username = current_username
        self._build_ui()

    def _build_ui(self):
        # ── Encabezado ──────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(28, 20))

        ctk.CTkLabel(
            header,
            text="⚙️  Configuración",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=TEXT_1
        ).pack(side="left")

        # ── Tarjeta de formulario ─────────────────────────────────────────────
        form_card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                                 border_width=1, border_color=BORDER)
        form_card.pack(fill="x", padx=30)

        ctk.CTkLabel(
            form_card,
            text="Cambiar Credenciales",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color=TEXT_1
        ).pack(anchor="w", padx=24, pady=(20, 4))

        ctk.CTkLabel(
            form_card,
            text="Actualiza tu nombre de usuario y contraseña de acceso al sistema.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_3
        ).pack(anchor="w", padx=24, pady=(0, 18))

        # Campos
        fields = ctk.CTkFrame(form_card, fg_color="transparent")
        fields.pack(fill="x", padx=24, pady=(0, 12))
        fields.columnconfigure((0, 1), weight=1)

        def lbl(parent, col, text):
            ctk.CTkLabel(
                parent, text=text,
                font=ctk.CTkFont("Segoe UI", 11),
                text_color=TEXT_3
            ).grid(row=0, column=col, sticky="w",
                   padx=(0 if col == 0 else 16, 0), pady=(0, 4))

        def entry(parent, col, placeholder, show=""):
            e = ctk.CTkEntry(
                parent, placeholder_text=placeholder, show=show,
                height=40, corner_radius=8,
                border_color=BORDER, fg_color="#0f1117",
                text_color=TEXT_1, font=ctk.CTkFont("Segoe UI", 12)
            )
            e.grid(row=1, column=col, sticky="ew",
                   padx=(0 if col == 0 else 16, 0))
            return e

        lbl(fields, 0, "Nuevo Usuario")
        lbl(fields, 1, "Nueva Contraseña")

        self.entry_username = entry(fields, 0, "Ej: admin2")
        self.entry_username.insert(0, self.current_username)
        self.entry_password = entry(fields, 1, "••••••••", show="•")

        # Botón Guardar
        btn = ctk.CTkButton(
            form_card, text="Guardar Cambios",
            height=42, corner_radius=8,
            fg_color="#0ea5e9", hover_color="#0284c7",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 13, "bold"),
            command=self.on_save
        )
        btn.pack(padx=24, pady=(8, 8), fill="x")

        self.lbl_status = ctk.CTkLabel(
            form_card, text="", font=ctk.CTkFont("Segoe UI", 11)
        )
        self.lbl_status.pack(padx=24, pady=(0, 16), anchor="w")

    def on_save(self):
        new_user = self.entry_username.get().strip()
        new_pass = self.entry_password.get()

        if not new_user or not new_pass:
            self.lbl_status.configure(
                text="⚠  Error: Ambos campos son requeridos.",
                text_color=RED_ERR
            )
            return

        try:
            update_credentials(self.current_username, new_user, new_pass)
            self.current_username = new_user  # update internal state
            self.lbl_status.configure(
                text="✓  Credenciales actualizadas correctamente.",
                text_color=GREEN
            )
        except Exception as e:
            self.lbl_status.configure(
                text=f"⚠  Error al actualizar: {str(e)}",
                text_color=RED_ERR
            )

    def refresh(self):
        # En caso de que se necesite refrescar estado
        pass
