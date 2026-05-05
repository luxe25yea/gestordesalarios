from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf_report(data, chart_image_path, output_path="reporte.pdf"):
    """Genera un reporte PDF con la tabla de salarios y la gráfica."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    elements.append(Paragraph("Reporte de Salarios - Aguas Moya", styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Tabla de datos
    table_data = [['Nombre', 'Salario Total']]
    for item in data:
        table_data.append([item['nombre'], f"${item['total_pago']:.2f}"])
        
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Gráfica
    if os.path.exists(chart_image_path):
        img = Image(chart_image_path, width=400, height=250)
        elements.append(img)
        
    doc.build(elements)
