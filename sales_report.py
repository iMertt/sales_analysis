from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

def generate_pdf_report(analyzer):
    doc = SimpleDocTemplate("sales_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    elements.append(Paragraph("Sales Analysis Report", styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Add top products
    elements.append(Paragraph("Top Products by Revenue", styles['Heading1']))
    top_products = analyzer.get_top_products(5)
    data = [["Product", "Revenue", "Quantity"]]
    for product, row in top_products.iterrows():
        data.append([product, f"${row['revenue']:,.2f}", row['quantity_sold']])
    
    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Add visualizations
    elements.append(Paragraph("Sales Visualizations", styles['Heading1']))
    elements.append(Image('monthly_sales.png', width=400, height=200))
    elements.append(Image('top_products.png', width=400, height=200))
    
    # Generate PDF
    doc.build(elements)