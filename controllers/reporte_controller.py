from services.nomina_service import get_report_data
from utils.charts import generate_salary_chart
from utils.pdf_generator import generate_pdf_report
import os

class ReporteController:
    def __init__(self, view):
        self.view = view
        
    def generate_report(self):
        data = get_report_data()
        if not data:
            self.view.show_error("Error", "No hay datos para generar el reporte.")
            return
            
        chart_path = generate_salary_chart(data)
        
        self.view.show_message("Generando...", "Generando PDF y Gráfica...")
        
        pdf_path = os.path.join(os.getcwd(), "reporte_salarios.pdf")
        generate_pdf_report(data, chart_path, pdf_path)
        
        self.view.show_message("Éxito", f"Reporte exportado a PDF en:\n{pdf_path}")
