import csv
from fpdf import FPDF
from datetime import datetime
import PyPDF2
import os

# Load Order Data from CSV
def load_order_data(file_name):
    orders = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            orders.append({
                'order_id': row['OrderID'],
                'customer_name': row['Customer Name'],
                'product_name': row['Product Name'],
                'quantity': int(row['Quantity']),
                'unit_price': float(row['Unit Price'])
            })
    return orders

# Create PDF invoice for each order
def create_pdf_invoice(order):
    # Create PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font
    pdf.set_font('Arial', 'B', 16)
    
    # Title and Invoice Number
    pdf.cell(200, 10, txt=f"Invoice - {order['order_id']}", ln=True, align='C')
    
    # Set font for details
    pdf.set_font('Arial', '', 12)
    
    # Add order details
    pdf.ln(10)
    pdf.cell(100, 10, f"Date of Purchase: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.ln(10)
    pdf.cell(100, 10, f"Customer Name: {order['customer_name']}")
    pdf.ln(10)
    pdf.cell(100, 10, f"Product Name: {order['product_name']}")
    pdf.ln(10)
    pdf.cell(100, 10, f"Quantity: {order['quantity']}")
    pdf.ln(10)
    pdf.cell(100, 10, f"Unit Price: ${order['unit_price']:.2f}")
    pdf.ln(10)
    total_amount = order['quantity'] * order['unit_price']
    pdf.cell(100, 10, f"Total Amount: ${total_amount:.2f}")
    
    # Output the PDF to a file
    pdf_file_name = f"invoice_{order['order_id']}.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name

# Merge all PDFs into a single PDF
def merge_pdfs(pdf_files, output_file="all_invoices.pdf"):
    merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            merger.append(pdf_file)
        else:
            print(f"Warning: PDF file {pdf_file} not found!")
    
    if pdf_files:  # Only merge if there are PDFs to merge
        merger.write(output_file)
        merger.close()
        print(f"PDFs merged successfully into {output_file}")
    else:
        print("No PDFs to merge!")

# Main Function
def main():
    # Load orders from CSV
    orders = load_order_data("orders.csv")
    
    # Generate individual PDF invoices and collect their file names
    pdf_files = []
    for order in orders:
        pdf_file = create_pdf_invoice(order)
        pdf_files.append(pdf_file)
    
    # Merge the generated PDF invoices into one
    merge_pdfs(pdf_files)

if __name__ == "__main__":
    main()
