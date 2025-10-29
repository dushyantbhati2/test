import io
from django.core.files.base import ContentFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from num2words import num2words
from reportlab.platypus import Image
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def generate_payslip_pdf(payroll):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    logo_path = os.path.join(BASE_DIR, "image", "logo.jpg")

    logo = Image(logo_path, width=400, height=70)
    logo.hAlign = "LEFT"

    elements.append(logo)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Payslip</b>", styles["Title"]))
   
    elements.append(Spacer(1, 20))

    emp_data = [
    ["Employee details",""],
    ["Date of Joining", str(payroll.employee.date_of_joining)],
    ["Employee Name", payroll.employee.name],
    ["Pay Month", payroll.pay_month],
    ["Transaction ID", payroll.transaction_id],
    ["Employment Type", payroll.employee.employment_type],
    ["Job Title", payroll.employee.job_title],
    ["Department", str(payroll.employee.department)],
    ["Email", payroll.employee.email],
]

    emp_table = Table(emp_data, colWidths=[180, 300])
    emp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(emp_table)
    elements.append(Spacer(1, 20))
    salary_data = [
        ["Earnings", "Amount", "Deductions", "Amount"],
        ["Basic Salary", f"{payroll.basic_salary}", "Deductions", f"{payroll.deductions}"],
        ["Allowances", f"{payroll.allowances}", "", ""],
        ["", "", "Total Deductions", f"{payroll.deductions}"],
        ["","","Net Salary", f"{payroll.net_salary}"],
    ]

    salary_table = Table(salary_data, colWidths=[120, 120, 120, 120])
    salary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))
    elements.append(salary_table)
    elements.append(Spacer(1, 20))
    netpay_data = [[
        Paragraph(
        f"<b>{payroll.net_salary} (in words: {num2words(payroll.net_salary)} only)</b>",
        styles["Normal"]
    )
    ]]

    netpay_table = Table(netpay_data, colWidths=[496])  
    netpay_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(netpay_table)
    elements.append(Spacer(1, 15))  


    signature_data = [
        ["__________________________", "__________________________"],
        ["Employer Signature", "Employee Signature"],
    ]

    signature_table = Table(signature_data, colWidths=[245, 245])
    signature_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
    ]))
    elements.append(signature_table)
    elements.append(Spacer(2, 30))
    footer_data = [["This is a system generated payslip"]]

    footer_table = Table(footer_data, colWidths=[496]) 
    footer_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(footer_table)

    doc.build(elements)

    buffer.seek(0)
    return ContentFile(buffer.read(), f"payslip_{payroll.employee.id}_{payroll.date}.pdf")
