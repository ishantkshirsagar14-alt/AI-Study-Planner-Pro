from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import TableStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor, PCMYKColor, Color
from io import BytesIO
import datetime

def generate_pdf(df):
    """
    Generate a beautifully styled PDF study plan with modern design
    """
    buffer = BytesIO()
    
    # Create document with custom page size and margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        title="AI Study Planner - Daily Plan",
        author="AI Study Planner Pro"
    )
    
    elements = []
    
    # -----------------------------
    # CUSTOM STYLES - MODERN DESIGN
    # -----------------------------
    styles = getSampleStyleSheet()
    
    # Add custom fonts and colors
    PRIMARY_COLOR = HexColor('#667eea')  # Purple
    SECONDARY_COLOR = HexColor('#764ba2')  # Dark Purple
    ACCENT_COLOR = HexColor('#38ef7d')  # Green
    WARNING_COLOR = HexColor('#ff6b6b')  # Red
    TEXT_DARK = HexColor('#2d3748')  # Dark Gray
    TEXT_LIGHT = HexColor('#718096')  # Light Gray
    BACKGROUND_COLOR = HexColor('#f7fafc')  # Off White
    
    # Title Style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica-Bold',
        leading=34
    ))
    
    # Subtitle Style
    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=TEXT_LIGHT,
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica',
        leading=18
    ))
    
    # Section Header Style
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        leading=22,
        borderWidth=0,
        borderColor=PRIMARY_COLOR,
        borderRadius=5
    ))
    
    # Table Header Style
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=14
    ))
    
    # Table Cell Style
    styles.add(ParagraphStyle(
        name='TableCell',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_DARK,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=13
    ))
    
    # Info Box Style
    styles.add(ParagraphStyle(
        name='InfoBox',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_DARK,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leading=16,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=5,
        spaceAfter=5
    ))
    
    # -----------------------------
    # HEADER SECTION
    # -----------------------------
    
    # App Title with Icon
    title_text = """
    <para alignment='center'>
        <font size=28 color='#667eea'><b>📚 AI STUDY PLANNER PRO</b></font>
    </para>
    """
    elements.append(Paragraph(title_text, styles['CustomTitle']))
    
    # Date and Generated Info
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    date_text = f"""
    <para alignment='center'>
        <font size=11 color='#718096'>Generated on {current_date} • Powered by Artificial Intelligence</font>
    </para>
    """
    elements.append(Paragraph(date_text, styles['Subtitle']))
    
    # Decorative Line
    d = Drawing(400, 10)
    d.add(Line(0, 5, 400, 5, strokeColor=PRIMARY_COLOR, strokeWidth=2, strokeDashArray=[5, 5]))
    elements.append(d)
    elements.append(Spacer(1, 0.2 * inch))
    
    # -----------------------------
    # STUDY PLAN SUMMARY CARD
    # -----------------------------
    
    elements.append(Paragraph("📋 DAILY STUDY ALLOCATION", styles['SectionHeader']))
    
    # Calculate summary statistics
    total_hours = df['Daily Allocated Hours'].sum() if 'Daily Allocated Hours' in df.columns else 0
    num_subjects = len(df)
    avg_hours = total_hours / num_subjects if num_subjects > 0 else 0
    max_subject = df.loc[df['Daily Allocated Hours'].idxmax(), 'Subject'] if 'Subject' in df.columns and 'Daily Allocated Hours' in df.columns else "N/A"
    
    # Create summary box
    summary_data = [
        ["📊 Total Daily Hours", f"{total_hours:.1f}h", "🎯 Target: Achieve daily goal"],
        ["📚 Number of Subjects", str(num_subjects), "⚡ Focus on weak areas"],
        ["⏰ Average per Subject", f"{avg_hours:.1f}h", f"📌 Priority: {max_subject}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0, 0), (0, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (1, 0), (1, -1), SECONDARY_COLOR),
        ('TEXTCOLOR', (2, 0), (2, -1), TEXT_LIGHT),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('BOX', (0, 0), (-1, -1), 2, PRIMARY_COLOR),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # -----------------------------
    # MAIN STUDY TABLE - BEAUTIFULLY STYLED
    # -----------------------------
    
    elements.append(Paragraph("🗓️ DETAILED STUDY SCHEDULE", styles['SectionHeader']))
    
    # Prepare table data with headers
    headers = [Paragraph(col, styles['TableHeader']) for col in df.columns]
    table_data = [headers]
    
    # Add rows with alternating colors
    for idx, row in df.iterrows():
        row_data = []
        for col in df.columns:
            value = row[col]
            if isinstance(value, float):
                value = f"{value:.1f} hrs"
            elif col == "Subject":
                value = f"📘 {value}"
            row_data.append(Paragraph(str(value), styles['TableCell']))
        table_data.append(row_data)
    
    # Calculate column widths
    col_widths = []
    for i, col in enumerate(df.columns):
        if col == "Subject":
            col_widths.append(2.2 * inch)
        elif "Hours" in col:
            col_widths.append(1.5 * inch)
        else:
            col_widths.append(1.8 * inch)
    
    # Create table with beautiful styling
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Enhanced table style
    table_style = TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 15),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
        
        # Body styling
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
        ('TEXTCOLOR', (0, 1), (-1, -1), TEXT_DARK),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
        
        # Grid styling
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, PRIMARY_COLOR),
        ('LINEABOVE', (0, 1), (-1, 1), 1, HexColor('#cbd5e0')),
        
        # Alternating row colors
        ('BACKGROUND', (0, 2), (-1, -1), HexColor('#ffffff')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f8f9fa')]),
        
        # Rounded corners effect
        ('BOX', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
    ])
    
    # Add hour column specific styling
    for i, col in enumerate(df.columns):
        if "Hours" in col:
            table_style.add('TEXTCOLOR', (i, 1), (i, -1), SECONDARY_COLOR)
            table_style.add('FONTNAME', (i, 1), (i, -1), 'Helvetica-Bold')
    
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # -----------------------------
    # STUDY TIPS SECTION
    # -----------------------------
    
    elements.append(Paragraph("💡 SMART STUDY TIPS", styles['SectionHeader']))
    
    # Create tips table with icons
    tips_data = [
        ["⏰", "Pomodoro Technique", "25 min study + 5 min break = 1 Pomodoro"],
        ["🎯", "Active Recall", "Test yourself regularly, don't just read"],
        ["📊", "Spaced Repetition", "Review material at increasing intervals"],
        ["💤", "Sleep Well", "7-8 hours sleep improves memory by 40%"],
        ["💧", "Stay Hydrated", "Water improves cognitive function"],
        ["🏃", "Take Breaks", "Short walks boost creativity and focus"],
    ]
    
    tips_table = Table(tips_data, colWidths=[0.5*inch, 1.8*inch, 4*inch])
    tips_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
        ('TEXTCOLOR', (1, 0), (1, -1), PRIMARY_COLOR),
        ('TEXTCOLOR', (2, 0), (2, -1), TEXT_DARK),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(tips_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # -----------------------------
    # MOTIVATIONAL QUOTE
    # -----------------------------
    
    quotes = [
        "The secret of getting ahead is getting started.",
        "Success is the sum of small efforts, repeated day in and day out.",
        "Your only limit is your mind.",
        "Consistency is more important than perfection.",
        "Small progress is still progress.",
    ]
    
    quote_text = f"""
    <para alignment='center'>
        <font size=12 color='#667eea'><i>✨ {quotes[hash(str(datetime.datetime.now())) % len(quotes)]} ✨</i></font>
    </para>
    """
    
    d = Drawing(400, 1)
    d.add(Line(0, 0, 400, 0, strokeColor=HexColor('#e2e8f0'), strokeWidth=1))
    elements.append(d)
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(quote_text, styles['Normal']))
    elements.append(Spacer(1, 0.1 * inch))
    d = Drawing(400, 1)
    d.add(Line(0, 0, 400, 0, strokeColor=HexColor('#e2e8f0'), strokeWidth=1))
    elements.append(d)
    
    # -----------------------------
    # FOOTER SECTION
    # -----------------------------
    
    elements.append(Spacer(1, 0.5 * inch))
    
    # Footer table with branding
    footer_data = [
        ["📚 AI Study Planner Pro", "🤖 Generated by AI", "👨‍💻 Developed by Ishant Kshirsagar"],
        ["", f"Page 1 of 1 • {current_date}", ""],
    ]
    
    footer_table = Table(footer_data, colWidths=[2.5*inch, 2.5*inch, 2*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, -1), TEXT_LIGHT),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, 0), PRIMARY_COLOR),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(footer_table)
    
    # Copyright
    copyright_text = """
<para alignment='center'>
    <font size=8 color='#a0aec0'>© 2026 Ishant Kshirsagar. All Rights Reserved. AI Study Planner Pro is developed and maintained by Ishant Kshirsagar. Made with ❤️ for students.</font>
</para>
"""
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(copyright_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer