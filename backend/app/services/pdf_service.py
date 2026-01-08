from fpdf import FPDF
from app.schemas.task import Task
from typing import List
import os

class TaskPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Tareas Diarias - 2026', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_tasks_pdf(tasks: List[Task], output_path: str):
    pdf = TaskPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Cabecera de la tabla
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(20, 10, "Fecha", 1, 0, 'C', 1)
    pdf.cell(60, 10, "Descripción", 1, 0, 'C', 1)
    pdf.cell(35, 10, "Categoría", 1, 0, 'C', 1)
    pdf.cell(15, 10, "Inicio", 1, 0, 'C', 1)
    pdf.cell(15, 10, "Fin", 1, 0, 'C', 1)
    pdf.cell(15, 10, "Hrs", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Estado", 1, 1, 'C', 1)

    for task in tasks:
        pdf.cell(20, 10, str(task.date), 1)
        desc = task.description[:35] + "..." if len(task.description) > 38 else task.description
        pdf.cell(60, 10, desc, 1)
        pdf.cell(35, 10, (task.category or "")[:18], 1)
        pdf.cell(15, 10, task.start_time or "", 1, 0, 'C')
        pdf.cell(15, 10, task.end_time or "", 1, 0, 'C')
        pdf.cell(15, 10, f"{task.duration:.1f}", 1, 0, 'C')
        pdf.cell(30, 10, task.status, 1, 1, 'C')

    pdf.output(output_path)
    return output_path
