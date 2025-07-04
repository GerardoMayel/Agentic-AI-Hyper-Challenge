#!/usr/bin/env python3
"""
Script para crear el PDF del formulario de claims y subirlo al storage.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Leer directamente el archivo .env y establecer DATABASE_URL
env_path = os.path.abspath('.env')
with open(env_path, 'r') as f:
    for line in f:
        if line.startswith('DATABASE_URL='):
            db_url = line.split('=', 1)[1].strip()
            os.environ['DATABASE_URL'] = db_url
            break

load_dotenv()

def crear_pdf_claim_form():
    """Crea el PDF del formulario de claims."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from io import BytesIO
    
    # Crear PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Contenido del PDF
    story = []
    
    # Título
    story.append(Paragraph("TRAVEL INSURANCE CLAIM FORM", title_style))
    story.append(Spacer(1, 20))
    
    # Información del claim
    story.append(Paragraph("CLAIM INFORMATION", section_style))
    claim_info_data = [
        ['Claim Number:', '_________________'],
        ['Date of Submission:', '_________________'],
        ['Policy Number:', '_________________']
    ]
    claim_table = Table(claim_info_data, colWidths=[2*inch, 3*inch])
    claim_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(claim_table)
    story.append(Spacer(1, 20))
    
    # Tipo de claim
    story.append(Paragraph("TYPE OF CLAIM", section_style))
    story.append(Paragraph("Please check the type of claim you are filing:", styles['Normal']))
    story.append(Spacer(1, 10))
    
    claim_types = [
        "☐ Trip Cancellation - For reimbursement of non-refundable trip payments when you cannot travel",
        "☐ Trip Delay - For reimbursement of out-of-pocket expenses due to an unforeseen delay",
        "☐ Trip Interruption - For reimbursement of unused trip portions or additional transportation costs",
        "☐ Baggage Delay - For reimbursement of essential item purchases when luggage is delayed"
    ]
    
    for claim_type in claim_types:
        story.append(Paragraph(claim_type, styles['Normal']))
        story.append(Spacer(1, 5))
    
    story.append(Spacer(1, 20))
    
    # Información del reclamante
    story.append(Paragraph("CLAIMANT INFORMATION", section_style))
    claimant_data = [
        ['Name of person completing form:', ''],
        ['Full names of all persons claiming:', ''],
        ['Email Address:', ''],
        ['Mobile Phone Number:', ''],
        ['Mailing Address:', ''],
        ['City:', 'State:', 'Postal Code:'],
        ['Name of Travel Agency/Company:', ''],
        ['Date of Initial Trip Deposit:', '']
    ]
    
    claimant_table = Table(claimant_data, colWidths=[2.5*inch, 2.5*inch])
    claimant_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(claimant_table)
    story.append(Spacer(1, 20))
    
    # Sobre lo que pasó
    story.append(Paragraph("ABOUT WHAT HAPPENED", section_style))
    story.append(Paragraph("Detailed description of the incident:", styles['Normal']))
    story.append(Spacer(1, 10))
    
    # Área para descripción
    incident_data = [
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', '']
    ]
    incident_table = Table(incident_data, colWidths=[5*inch])
    incident_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(incident_table)
    story.append(Spacer(1, 10))
    
    # Fecha de pérdida y monto
    loss_data = [
        ['Date of Loss:', 'Total Amount Requested for Reimbursement (USD):'],
    ]
    loss_table = Table(loss_data, colWidths=[2.5*inch, 2.5*inch])
    loss_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(loss_table)
    story.append(Spacer(1, 20))
    
    # Desglose de gastos
    story.append(Paragraph("BREAKDOWN OF EXPENSES", section_style))
    expense_headers = ['Description of Expense', 'Date', 'Amount (USD)']
    expense_data = [expense_headers]
    
    # Agregar filas vacías para gastos
    for i in range(5):
        expense_data.append(['', '', ''])
    
    expense_table = Table(expense_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
    expense_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ]))
    story.append(expense_table)
    story.append(Spacer(1, 20))
    
    # Documentos adjuntos
    story.append(Paragraph("DOCUMENT UPLOAD", section_style))
    story.append(Paragraph("Please attach the following documents (if applicable):", styles['Normal']))
    story.append(Spacer(1, 10))
    
    documents_list = [
        "• Receipts for all expenses",
        "• Travel itinerary",
        "• Police reports (if applicable)",
        "• Medical certificates (if applicable)",
        "• Any other relevant documentation"
    ]
    
    for doc in documents_list:
        story.append(Paragraph(doc, styles['Normal']))
        story.append(Spacer(1, 5))
    
    story.append(Spacer(1, 20))
    
    # Autorización y firma
    story.append(Paragraph("AUTHORIZATION & SIGNATURE", section_style))
    story.append(Paragraph("☐ I agree to the terms and conditions of this claim submission.", styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Signature (Type your full name):", styles['Normal']))
    story.append(Spacer(1, 10))
    
    # Línea para firma
    signature_data = [['', '']]
    signature_table = Table(signature_data, colWidths=[5*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ]))
    story.append(signature_table)
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def subir_pdf_al_storage():
    """Sube el PDF del formulario al storage en ubicación fija."""
    try:
        print("📄 Creando PDF del formulario de claims...")
        pdf_content = crear_pdf_claim_form()
        print(f"✅ PDF creado: {len(pdf_content)} bytes")
        
        # Inicializar servicio de storage
        print("\n☁️ Subiendo PDF al storage...")
        from app.services.gcs_storage import gcs_storage
        
        if not gcs_storage.bucket:
            print("❌ Error: No se pudo conectar a Google Cloud Storage")
            return False
        
        # Ubicación fija para el PDF
        filename = "Travel_Insurance_Claim_Form.pdf"
        storage_path = f"forms/{filename}"
        
        # Crear blob y subir
        blob = gcs_storage.bucket.blob(storage_path)
        blob.upload_from_string(pdf_content, content_type="application/pdf")
        
        # Generar URL
        url = f"https://storage.googleapis.com/{gcs_storage.bucket_name}/{storage_path}"
        
        print(f"✅ PDF subido exitosamente")
        print(f"   URL: {url}")
        print(f"   Ruta: {storage_path}")
        print(f"   Ubicación fija: forms/Travel_Insurance_Claim_Form.pdf")
        
        return url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Función principal."""
    print("🚀 CREACIÓN Y SUBIDA DEL PDF DE FORMULARIO DE CLAIMS")
    print("=" * 60)
    
    # Preguntar confirmación
    confirmacion = input("¿Deseas crear y subir el PDF del formulario? (y/N): ").strip().lower()
    
    if confirmacion in ['y', 'yes', 'sí', 'si']:
        url = subir_pdf_al_storage()
        if url:
            print("\n🎉 ¡PDF del formulario creado y subido exitosamente!")
            print(f"   URL permanente: {url}")
            print("   Este PDF estará disponible para todos los claims.")
        else:
            print("\n❌ Error creando/subiendo el PDF")
    else:
        print("\n⚠️ Operación cancelada")

if __name__ == "__main__":
    main() 