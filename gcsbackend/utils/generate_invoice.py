import io
from decimal import Decimal
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)
from invoice.models import Invoice
from num2words import num2words
from reportlab.lib.enums import TA_CENTER

def generate_invoice_pdf(invoice: Invoice, save_to_model=True):
    """
    Generate an invoice PDF with a professional layout, based on the provided sample.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5 * cm,
        bottomMargin=0.5 * cm,
        leftMargin=1 * cm,
        rightMargin=1 * cm
    )
    elements = []
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))
    styles.add(ParagraphStyle(name='Left', alignment=0))
    
    # Define custom styles
    # Smaller font for most text
    normal_style = ParagraphStyle(name='Normal', parent=styles['Normal'], fontSize=9, leading=11)
    # Slightly larger for headings
    ParagraphStyle(name='Heading', parent=styles['Normal'], fontSize=10, leading=12)
    center_style = ParagraphStyle(
        name="CenterStyle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
    )

    # =================================================================
    # Helper function to convert number to words
    # =================================================================
    def amount_in_words(num):
        """Converts a number to words (Indian currency format)."""
        if num is None: 
            return ""
        num_str = f"{Decimal(num):.2f}"
        integer_part_str, decimal_part_str = num_str.split('.')
        integer_part = int(integer_part_str)
        words = num2words(integer_part, lang='en_IN').title()
        return f"INR {words} Only"

    # ======================================================
    # 1. HEADER SECTION
    # ======================================================
    elements.append(Paragraph("<b>Tax Invoice</b>", styles['Center']))
    elements.append(Spacer(1, 0.2*cm))

    company_details = [
        Paragraph("<b>GLOBAL CONSULTANCY SERVICES</b>", center_style),
        Spacer(1, 4),
        Paragraph("016, Loha Bhavan, P D'Mello Road, Carnac Bunder, Masjid (E), Mumbai - 400009", center_style),
        Spacer(1, 4),
        Paragraph("<b>GSTIN/UIN:</b> 27AINPA9487A1Z4", center_style),
        Spacer(1, 4),
        Paragraph("<b>State Name:</b> Maharashtra, Code: 27", center_style),
        Spacer(1, 4),
        Paragraph("<b>Email:</b> admin@globalconsultancyservices.net", center_style),
    ]

    header_table = Table([[company_details]], colWidths=[18 * cm],hAlign='CENTER')
    header_table.setStyle(TableStyle([( 'VALIGN', (0, 0), (-1, -1), 'TOP')]))
    elements.append(header_table)

    # ======================================================
    # 2. BUYER AND INVOICE DETAILS
    # ======================================================
    client = invoice.customer
    address = client.addresses.first()
    contact = client.contacts.first()

    buyer_details = [
        [Paragraph("<u>Client Details:</u>", normal_style)],
        [Paragraph(f"<b>{client.company_name}</b>", normal_style)],
        [Paragraph(f"{address.city}, {address.state},{address.country} - {address.postal_code}", normal_style)],
        [Paragraph(f"<b>Client Name: </b> {contact.first_name} {contact.last_name}", normal_style)],
        [Paragraph(f"<b>State Name:</b> {address.state}", normal_style)],
        [Paragraph(f"<b>Client GSTIN/UIN:</b> {client.gst_number}", normal_style)],
        ]
    buyer_table = Table(buyer_details, colWidths=[9*cm])
    buyer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    invoice_details_content = [
        [Paragraph(f"<b>Invoice No:</b> {invoice.invoice_no}", normal_style)],
        [Paragraph(f"<b>Date:</b> {invoice.invoice_date.strftime('%d-%b-%y')}", normal_style)],
        [Paragraph(f"<b>P.O. No:</b> {invoice.po_no or '-'}", normal_style)],
        [Paragraph(f"<b>Our Ref.:</b> {invoice.our_ref}", normal_style)],
        [Paragraph(f"<b>Place of Supply:</b> {invoice.place_of_supply}", normal_style)],
        [Paragraph(f"<b>Vessel Name:</b> {invoice.vessel.name if invoice.vessel else '-'}", normal_style)],
        ]
    invoice_table = Table(invoice_details_content, colWidths=[9*cm])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    parties_table = Table([[buyer_table, invoice_table]], colWidths=[9*cm, 9*cm],hAlign='LEFT')
    parties_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(parties_table)

    elements.append(Spacer(1, 0.2*cm))
    # ======================================================
# 3. SERVICES/ITEMS TABLE (without "Per" column)
# ======================================================
    items_header = [
        Paragraph("<b>Sr.<br/>No.</b>", styles['Center']),
        Paragraph("<b>Particulars</b>", styles['Center']),
        Paragraph("<b>Qty</b>", styles['Center']),
        Paragraph("<b>Rate</b>", styles['Center']),
        Paragraph("<b>Amount</b>", styles['Center']),
    ]
    items_data = [items_header]

    subtotal = Decimal("0.00")
    for idx, item in enumerate(invoice.items.all(), start=1):
        row = [
            Paragraph(str(idx), styles['Center']),
            Paragraph(item.description, normal_style),
                Paragraph(str(item.quantity), styles['Center']),
            Paragraph(f"{item.unit_price:.2f}", styles['Right']),
            Paragraph(f"{item.amount:.2f}", styles['Right']),
        ]
        subtotal += item.amount
        items_data.append(row)

    # Tax calculations
    cgst_rate = Decimal(invoice.cgst)
    sgst_rate = Decimal(invoice.sgst)
    igst_rate = Decimal(invoice.igst)
    cgst = subtotal * cgst_rate / Decimal("100.00")
    sgst = subtotal * sgst_rate / Decimal("100.00")
    igst = subtotal * igst_rate / Decimal("100.00")
    grand_total = subtotal + cgst + sgst + igst

    for _ in range(max(0, 10 - len(invoice.items.all()))):
        items_data.append(['', '', '', '', ''])

    # Summary rows (span first 5 columns, put value in last col)
    summary_style_right = ParagraphStyle(name='summary_right', parent=styles['Right'], fontSize=9)
    items_data.extend([
        [Paragraph("Sub Total", summary_style_right),  '', '', '', Paragraph(f"{subtotal:.2f}", summary_style_right)],
        [Paragraph(f"Add: CGST @{cgst_rate}%", summary_style_right),  '', '', '', Paragraph(f"{cgst:.2f}", summary_style_right)],
        [Paragraph(f"Add: SGST @{sgst_rate}%", summary_style_right),  '', '', '', Paragraph(f"{sgst:.2f}", summary_style_right)],
        [Paragraph(f"Add: IGST @{igst_rate}%", summary_style_right),  '', '', '', Paragraph(f"{igst:.2f}", summary_style_right)],
        [Paragraph("<b>Grand Total</b>", summary_style_right), '', '', '', Paragraph(f"<b>{grand_total:.2f}</b>", summary_style_right)],
    ])

    items_table = Table(
        items_data,
        colWidths=[1*cm, 10*cm, 2*cm, 2.5*cm, 2.5*cm, 3*cm],
        rowHeights=[1*cm] + [None] * (len(items_data) - 1)
    )
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        # Spanning cells for summary rows (now col 0 → col 4)
        ('SPAN', (0, -5), (3, -5)), # Sub Total
        ('SPAN', (0, -4), (3, -4)), # CGST
        ('SPAN', (0, -3), (3, -3)), # SGST
        ('SPAN', (0, -2), (3, -2)), # IGST
        ('SPAN', (0, -1), (3, -1)), # Grand Total
    ]))
    elements.append(items_table)

    
    # ======================================================
    # 4. AMOUNT IN WORDS & BANK DETAILS
    # ======================================================
    indented_style = ParagraphStyle(
        "Indented",
        parent=normal_style,
        leftIndent=10  
    )
    amount_words_para = Paragraph(f"<b>Amount Chargeable (in words):</b>{amount_in_words(grand_total)}", indented_style)
    elements.append(Spacer(1, 0.2*cm))
    elements.append(amount_words_para)
    elements.append(Spacer(1, 0.2*cm))
    
    bank_details_content = [
        Paragraph("<u>Bank Details</u>", normal_style),
        Spacer(1,4),
        Paragraph("<b>Bank Name:</b> ICICI BANK LTD.", normal_style),
        Spacer(1,4),
        Paragraph("<b>A/c No:</b> 124905500046", normal_style),
        Spacer(1,4),
        Paragraph("<b>GSTIN:</b> 27AINPA9487A1Z4", normal_style),
        Spacer(1,4),
        Paragraph("<b>HSN/SAC:</b> 99812", normal_style),
        Spacer(1,4),
        Paragraph("<b>Branch & IFSC:</b> VIKHROLI (EAST) & ICIC0001249", normal_style),
        Spacer(1,4),
        Paragraph("<b>PAN No.:</b> AINPA9487A", normal_style)
    ]

    declaration_content = [
        Paragraph("<u>Payment Terms :</u>", normal_style),
        Spacer(1,4),
        Paragraph("Interest @ 21% Per annum will be charged if not paid within 30 days or specifically agreed in Contract.", normal_style)
    ]

    bank_declaration_table = Table([[bank_details_content, declaration_content]], colWidths=[9*cm, 9*cm])
    bank_declaration_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(bank_declaration_table)

    # ======================================================
    # 5. FOOTER & SIGNATURE
    # ======================================================
    signature_content = [
        Paragraph("For, <b>GLOBAL CONSULTANCY SERVICES</b>", styles['Center']),
        Spacer(1, 70),
        Paragraph("______________________", styles['Center']),
        Paragraph("Authorised Signatory", styles['Center']),
    ]
    
    # Using a table to align signature to the right
    signature_table = Table([['', signature_content]], colWidths=[11*cm, 7*cm])
    signature_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))

    elements.append(signature_table)
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph("<i>This is a Computer Generated Invoice</i>", styles['Center']))

    # ======================================================
    # Build PDF
    # ======================================================
    doc.build(elements)
    buffer.seek(0)
    
    pdf_content = buffer.getvalue()
    buffer.close()

    # Save to model if requested
    if save_to_model:
        filename = f"{invoice.invoice_no}.pdf"
        invoice.pdf.save(filename, ContentFile(pdf_content), save=True)

    # Return a ContentFile for compatibility with FileResponse
    return ContentFile(pdf_content, name=f"{invoice.invoice_no}.pdf")
