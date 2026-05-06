"""
generar_reporte_tecnico.py
Genera el Reporte Técnico del proyecto en PDF usando ReportLab.
Ejecutar desde la carpeta aguas_moya/:
    python generar_reporte_tecnico.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "Reporte_Tecnico_AguasMoya.pdf"

# ── Paleta ────────────────────────────────────────────────────────────────────
AZUL       = colors.HexColor("#0ea5e9")
AZUL_OSC   = colors.HexColor("#0369a1")
GRIS_OSC   = colors.HexColor("#1e293b")
GRIS_MED   = colors.HexColor("#334155")
GRIS_CLAR  = colors.HexColor("#f1f5f9")
VERDE      = colors.HexColor("#16a34a")
BLANCO     = colors.white
NEGRO      = colors.HexColor("#0f172a")


def build_styles():
    base = getSampleStyleSheet()

    titulo_portada = ParagraphStyle(
        "TituloPortada", parent=base["Title"],
        fontSize=26, textColor=BLANCO, leading=32,
        alignment=TA_CENTER, spaceAfter=6
    )
    subtitulo_portada = ParagraphStyle(
        "SubPortada", parent=base["Normal"],
        fontSize=13, textColor=colors.HexColor("#94a3b8"),
        alignment=TA_CENTER, spaceAfter=4
    )
    h1 = ParagraphStyle(
        "H1", parent=base["Heading1"],
        fontSize=16, textColor=AZUL_OSC,
        spaceBefore=18, spaceAfter=6, leading=20
    )
    h2 = ParagraphStyle(
        "H2", parent=base["Heading2"],
        fontSize=13, textColor=GRIS_OSC,
        spaceBefore=12, spaceAfter=4, leading=16
    )
    body = ParagraphStyle(
        "Body", parent=base["Normal"],
        fontSize=10, textColor=NEGRO,
        leading=16, spaceAfter=6, alignment=TA_JUSTIFY
    )
    code = ParagraphStyle(
        "Code", parent=base["Code"],
        fontSize=9, textColor=colors.HexColor("#1e40af"),
        backColor=colors.HexColor("#eff6ff"),
        leftIndent=12, rightIndent=12,
        borderPad=4, spaceAfter=8
    )
    bullet = ParagraphStyle(
        "Bullet", parent=base["Normal"],
        fontSize=10, textColor=NEGRO, leading=15,
        leftIndent=20, bulletIndent=8, spaceAfter=3
    )
    return {
        "titulo_portada": titulo_portada,
        "subtitulo_portada": subtitulo_portada,
        "h1": h1, "h2": h2,
        "body": body, "code": code, "bullet": bullet
    }


def portada(s):
    """Página de portada."""
    items = []

    # Fondo de portada simulado con tabla de color
    portada_table = Table(
        [[Paragraph("💧 Aguas Moya", s["titulo_portada"]),],
         [Paragraph("Sistema de Gestión de Jornadas y Salarios", s["subtitulo_portada"])],
         [Paragraph("Reporte Técnico de Proyecto", s["subtitulo_portada"])],
         [Spacer(1, 10)],
         [Paragraph("Materia: Programación en Python", s["subtitulo_portada"])],
         [Paragraph("Mayo 2025", s["subtitulo_portada"])],
        ],
        colWidths=[16 * cm]
    )
    portada_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_OSC),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [GRIS_OSC]),
        ("BOX",        (0, 0), (-1, -1), 2, AZUL),
        ("TOPPADDING",    (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))

    items.append(Spacer(1, 3 * cm))
    items.append(portada_table)
    items.append(Spacer(1, 1 * cm))
    return items


def seccion_intro(s):
    items = [
        Paragraph("1. Introducción", s["h1"]),
        HRFlowable(width="100%", thickness=1, color=AZUL, spaceAfter=8),
        Paragraph(
            "Aguas Moya es un sistema de escritorio desarrollado en Python que permite a pequeñas y "
            "medianas empresas del sector hídrico gestionar de forma eficiente su capital humano. "
            "La aplicación centraliza el registro de empleados, el control de asistencias y jornadas "
            "trabajadas, el cálculo automático de salarios y la generación de reportes visuales y en PDF.",
            s["body"]
        ),
        Paragraph(
            "El problema que resuelve es la gestión manual en hojas de cálculo o papel, que genera "
            "errores en el cálculo de nómina, dificulta el seguimiento histórico de asistencias y no "
            "ofrece visibilidad rápida del estado financiero del área de personal.",
            s["body"]
        ),
        Paragraph("<b>Objetivo principal:</b> Proveer una herramienta de gestión integral, segura, "
                  "intuitiva y ejecutable localmente sin depender de servicios externos.", s["body"]),
    ]
    return items


def seccion_diseno(s):
    # ── Tabla ER ─────────────────────────────────────────────────────────────
    er_data = [
        ["Tabla", "Campo", "Tipo", "Descripción"],
        ["usuarios",    "id",             "INTEGER PK",  "Identificador único"],
        ["",            "username",       "TEXT UNIQUE", "Nombre de usuario"],
        ["",            "password_hash",  "TEXT",        "Contraseña SHA-256"],
        ["empleados",   "id",             "INTEGER PK",  "Identificador único"],
        ["",            "nombre",         "TEXT",        "Nombre completo"],
        ["",            "puesto",         "TEXT",        "Cargo / Rol"],
        ["",            "salario_diario", "REAL",        "Salario por día ($)"],
        ["asistencias", "id",             "INTEGER PK",  "Identificador único"],
        ["",            "empleado_id",    "INTEGER FK",  "→ empleados.id"],
        ["",            "fecha",          "TEXT",        "Fecha (YYYY-MM-DD)"],
        ["",            "dias_trabajados","REAL",        "Días trabajados"],
    ]

    er_style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  AZUL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [GRIS_CLAR, BLANCO]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ])

    er_table = Table(er_data, colWidths=[3.5*cm, 4*cm, 3.5*cm, 5*cm])
    er_table.setStyle(er_style)

    # ── Tabla navegación GUI ──────────────────────────────────────────────────
    nav_data = [
        ["Pantalla",     "Accede desde",        "Funcionalidad"],
        ["Login",        "Inicio (main.py)",     "Autenticación de usuario"],
        ["Dashboard",    "Login exitoso",        "Resumen KPIs y tabla de empleados"],
        ["Empleados",    "Sidebar → Empleados",  "CRUD completo de empleados"],
        ["Jornadas",     "Sidebar → Jornadas",   "Registro de días trabajados"],
        ["Reportes",     "Sidebar → Reportes",   "Gráfica de nómina y exportar PDF"],
    ]
    nav_style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  AZUL_OSC),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [GRIS_CLAR, BLANCO]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ])
    nav_table = Table(nav_data, colWidths=[4*cm, 5.5*cm, 6.5*cm])
    nav_table.setStyle(nav_style)

    items = [
        Spacer(1, 0.3*cm),
        Paragraph("2. Diseño", s["h1"]),
        HRFlowable(width="100%", thickness=1, color=AZUL, spaceAfter=8),

        Paragraph("2.1 Diagrama Entidad-Relación (Esquema de BD)", s["h2"]),
        Paragraph(
            "La base de datos SQLite contiene tres tablas relacionadas entre sí. "
            "La tabla <b>asistencias</b> actúa como tabla de hechos y referencia a "
            "<b>empleados</b> mediante una clave foránea.",
            s["body"]
        ),
        er_table,
        Spacer(1, 0.5*cm),

        Paragraph("2.2 Diagrama de Navegación de la GUI", s["h2"]),
        Paragraph(
            "La aplicación sigue un flujo lineal desde el login hasta el dashboard, "
            "con navegación lateral mediante sidebar para acceder a cada módulo.",
            s["body"]
        ),
        nav_table,
        Spacer(1, 0.5*cm),

        Paragraph("2.3 Arquitectura del Software", s["h2"]),
        Paragraph(
            "El proyecto sigue el patrón <b>MVC (Modelo – Vista – Controlador)</b> "
            "dividido en capas independientes:",
            s["body"]
        ),
        Paragraph("• <b>Models</b>: Clases de datos (Usuario, Empleado, Asistencia)", s["bullet"]),
        Paragraph("• <b>Services</b>: Lógica de negocio y acceso a BD (auth, empleado, nómina)", s["bullet"]),
        Paragraph("• <b>Controllers</b>: Mediadores entre vistas y servicios", s["bullet"]),
        Paragraph("• <b>Views</b>: Interfaces CustomTkinter (login, dashboard, empleados, jornadas, reportes)", s["bullet"]),
        Paragraph("• <b>Utils</b>: Funciones auxiliares (hash, charts, pdf_generator)", s["bullet"]),
    ]
    return items


def seccion_tecnologias(s):
    tech_data = [
        ["Librería",       "Versión",  "Uso en el proyecto"],
        ["customtkinter",  "≥ 5.2",    "Interfaz gráfica moderna con modo oscuro"],
        ["matplotlib",     "≥ 3.8",    "Gráfica de barras de nómina por empleado"],
        ["reportlab",      "≥ 4.0",    "Generación de reportes en formato PDF"],
        ["sqlite3",        "Builtin",  "Base de datos local embebida"],
        ["hashlib",        "Builtin",  "Hash SHA-256 de contraseñas"],
        ["os / sys",       "Builtin",  "Gestión de rutas y módulos"],
        ["datetime",       "Builtin",  "Manejo de fechas en asistencias"],
    ]
    tech_style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  AZUL),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  BLANCO),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [GRIS_CLAR, BLANCO]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ])
    tech_table = Table(tech_data, colWidths=[4*cm, 3*cm, 9*cm])
    tech_table.setStyle(tech_style)

    items = [
        Spacer(1, 0.3*cm),
        Paragraph("3. Tecnologías Utilizadas", s["h1"]),
        HRFlowable(width="100%", thickness=1, color=AZUL, spaceAfter=8),
        Paragraph(
            "El proyecto fue desarrollado en Python 3.11 y hace uso exclusivo de "
            "librerías de código abierto. No requiere instalación de servidores externos.",
            s["body"]
        ),
        tech_table,
    ]
    return items


def seccion_instrucciones(s):
    pasos = [
        ("1. Clonar o descargar el proyecto",
         'git clone https://github.com/tu_usuario/aguas_moya.git\ncd aguas_moya'),
        ("2. Crear entorno virtual (recomendado)",
         'python -m venv venv\nvenv\\Scripts\\activate   # Windows'),
        ("3. Instalar dependencias",
         'pip install -r requirements.txt'),
        ("4. Cargar datos de prueba",
         'python seed_data.py'),
        ("5. Ejecutar la aplicación",
         'python main.py'),
    ]

    items = [
        Spacer(1, 0.3*cm),
        Paragraph("4. Instrucciones de Uso", s["h1"]),
        HRFlowable(width="100%", thickness=1, color=AZUL, spaceAfter=8),
        Paragraph(
            "Sigue los siguientes pasos en orden para instalar y ejecutar la aplicación "
            "correctamente en cualquier sistema con Python 3.10+.",
            s["body"]
        ),
    ]

    for titulo, cmd in pasos:
        items.append(Paragraph(f"<b>{titulo}</b>", s["body"]))
        items.append(Paragraph(cmd.replace("\n", "<br/>"), s["code"]))
        items.append(Spacer(1, 0.15*cm))

    items += [
        Paragraph("<b>Credenciales por defecto:</b>", s["body"]),
        Paragraph("• Usuario: <b>admin</b>", s["bullet"]),
        Paragraph("• Contraseña: <b>admin123</b>", s["bullet"]),
        Spacer(1, 0.5*cm),
        Paragraph("4.1 Flujo de uso de la aplicación", s["h2"]),
        Paragraph("• Ejecutar <b>main.py</b> → aparece la pantalla de Login.", s["bullet"]),
        Paragraph("• Ingresar credenciales → se abre el Dashboard con KPIs.", s["bullet"]),
        Paragraph("• Ir a <b>Empleados</b> en el sidebar → agregar, editar o eliminar empleados.", s["bullet"]),
        Paragraph("• Ir a <b>Jornadas</b> → registrar días trabajados por empleado.", s["bullet"]),
        Paragraph("• Ir a <b>Reportes</b> → generar gráfica de nómina o exportar PDF.", s["bullet"]),
        Spacer(1, 0.5*cm),
        Paragraph("4.2 Estructura de archivos generados", s["h2"]),
        Paragraph("• <b>data/aguas_moya.db</b>: Base de datos SQLite (auto-creada al primer inicio).", s["bullet"]),
        Paragraph("• <b>reporte_salarios.pdf</b>: Exportado en el directorio raíz al presionar «Exportar PDF».", s["bullet"]),
        Paragraph("• <b>temp_chart.png</b>: Imagen temporal de la gráfica usada en el PDF.", s["bullet"]),
    ]
    return items


def generar_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm,   bottomMargin=2*cm,
        title="Reporte Técnico – Aguas Moya",
        author="Equipo de desarrollo"
    )

    s = build_styles()
    story = []

    story += portada(s)
    story.append(Spacer(1, 1.5*cm))
    story += seccion_intro(s)
    story += seccion_diseno(s)
    story += seccion_tecnologias(s)
    story += seccion_instrucciones(s)

    doc.build(story)
    print(f"✅ Reporte técnico generado: {OUTPUT}")


if __name__ == "__main__":
    generar_pdf()
