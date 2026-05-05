import customtkinter as ctk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controllers.reporte_controller import ReporteController
from services.nomina_service import get_report_data

BG_DARK  = "#0f1117"
CARD_BG  = "#1e2535"
BORDER   = "#334155"
ACCENT   = "#38bdf8"
TEXT_1   = "#f1f5f9"
TEXT_2   = "#94a3b8"
TEXT_3   = "#64748b"
RED_ERR  = "#f87171"
GREEN    = "#4ade80"

class ReportesView(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_DARK, scrollbar_button_color=BORDER, **kwargs)
        self.controller = ReporteController(self)
        self._chart_canvas = None
        self._build_ui()

    def _build_ui(self):
        # ── Encabezado ──────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(28, 20))

        ctk.CTkLabel(
            header,
            text="📊  Reportes y Nómina",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=TEXT_1
        ).pack(side="left")

        # ── Tarjeta de acciones ───────────────────────────────────────────────
        actions_card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                                    border_width=1, border_color=BORDER)
        actions_card.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(
            actions_card,
            text="Generar Reportes",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            text_color=TEXT_1
        ).pack(anchor="w", padx=24, pady=(20, 6))

        ctk.CTkLabel(
            actions_card,
            text="Genera la gráfica de salarios o exporta el reporte completo a PDF.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_3
        ).pack(anchor="w", padx=24, pady=(0, 16))

        btn_row = ctk.CTkFrame(actions_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=24, pady=(0, 20))

        self.btn_grafica = ctk.CTkButton(
            btn_row, text="📊  Generar Gráfica",
            height=42, width=190, corner_radius=8,
            fg_color="#0ea5e9", hover_color="#0284c7",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 12, "bold"),
            command=self.on_grafica
        )
        self.btn_grafica.pack(side="left", padx=(0, 12))

        self.btn_pdf = ctk.CTkButton(
            btn_row, text="📄  Exportar a PDF",
            height=42, width=190, corner_radius=8,
            fg_color="#7c3aed", hover_color="#6d28d9",
            text_color="#fff", font=ctk.CTkFont("Segoe UI", 12, "bold"),
            command=self.on_pdf
        )
        self.btn_pdf.pack(side="left")

        self.lbl_status = ctk.CTkLabel(
            actions_card, text="", font=ctk.CTkFont("Segoe UI", 11)
        )
        self.lbl_status.pack(anchor="w", padx=24, pady=(0, 16))

        # ── Tarjeta de gráfica ────────────────────────────────────────────────
        self.chart_card = ctk.CTkFrame(self, corner_radius=14, fg_color=CARD_BG,
                                       border_width=1, border_color=BORDER)
        self.chart_card.pack(fill="both", padx=30, pady=(0, 24), expand=True)

        ctk.CTkLabel(
            self.chart_card,
            text="Salario Total por Empleado",
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            text_color=TEXT_1
        ).pack(anchor="w", padx=24, pady=(18, 4))

        ctk.CTkLabel(
            self.chart_card,
            text="Suma de salario diario × días trabajados por cada empleado.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_3
        ).pack(anchor="w", padx=24, pady=(0, 12))

        self.chart_placeholder = ctk.CTkLabel(
            self.chart_card,
            text="Presiona «Generar Gráfica» para visualizar los datos.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=TEXT_3
        )
        self.chart_placeholder.pack(pady=40)

    # ── Eventos ───────────────────────────────────────────────────────────────
    def on_grafica(self):
        try:
            data = get_report_data()
            if not data:
                self.show_error("", "Sin datos de nómina para graficar.")
                return
            self._render_chart(data)
            self.lbl_status.configure(text="✓  Gráfica generada.", text_color=GREEN)
        except Exception as e:
            self.show_error("", str(e))

    def on_pdf(self):
        self.controller.generate_report()

    # ── Renderizado de gráfica dentro de la ventana ────────────────────────────
    def _render_chart(self, data):
        # Limpiar gráfica anterior
        if self._chart_canvas:
            self._chart_canvas.get_tk_widget().destroy()
        if self.chart_placeholder.winfo_exists():
            self.chart_placeholder.pack_forget()

        nombres = [d["nombre"] for d in data]
        pagos   = [d["total_pago"] for d in data]

        colores = ["#38bdf8", "#4ade80", "#fb923c", "#a78bfa",
                   "#f472b6", "#facc15", "#34d399"]

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor("#1e2535")
        ax.set_facecolor("#1e2535")

        bars = ax.bar(nombres, pagos,
                      color=[colores[i % len(colores)] for i in range(len(nombres))],
                      width=0.55, edgecolor="none")

        # Etiquetas sobre cada barra
        for bar, val in zip(bars, pagos):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(pagos) * 0.02,
                f"${val:,.0f}",
                ha="center", va="bottom",
                fontsize=9, color="#f1f5f9"
            )

        ax.set_xlabel("Empleados", color="#94a3b8", fontsize=10)
        ax.set_ylabel("Salario Total ($)", color="#94a3b8", fontsize=10)
        ax.tick_params(colors="#94a3b8")
        ax.spines[:].set_color("#334155")
        ax.yaxis.grid(True, color="#263046", linestyle="--", linewidth=0.8)
        ax.set_axisbelow(True)

        plt.xticks(rotation=30, ha="right")
        plt.tight_layout(pad=2)

        self._chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_card)
        self._chart_canvas.draw()
        self._chart_canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=20, pady=(0, 20)
        )

    # ── Mensajes ──────────────────────────────────────────────────────────────
    def show_message(self, title, message):
        self.lbl_status.configure(text=f"✓  {message}", text_color=GREEN)

    def show_error(self, title, message):
        self.lbl_status.configure(text=f"⚠  {message}", text_color=RED_ERR)
