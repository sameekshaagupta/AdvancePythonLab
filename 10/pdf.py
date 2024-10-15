import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from PyPDF2 import PdfMerger

# Step 1: Load Order Data
def load_order_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Step 2: Generate PDF Invoice for each order
def generate_pdf_invoice(order, output_dir):
    order_id = order['OrderID']
    customer_name = order['CustomerName']
    product_name = order['ProductName']
    quantity = order['Quantity']
    unit_price = order['UnitPrice']
    total_amount = quantity * unit_price
    
    # Create invoice PDF
    invoice_filename = f"{output_dir}/Invoice_{order_id}.pdf"
    c = canvas.Canvas(invoice_filename, pagesize=A4)
    
    # Invoice content
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, f"Invoice Number: {order_id}")
    c.drawString(100, 780, f"Date of Purchase: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, 760, f"Customer Name: {customer_name}")
    c.drawString(100, 740, f"Product Name: {product_name}")
    c.drawString(100, 720, f"Quantity: {quantity}")
    c.drawString(100, 700, f"Unit Price: ${unit_price:.2f}")
    c.drawString(100, 680, f"Total Amount: ${total_amount:.2f}")
    
    c.showPage()
    c.save()

    return invoice_filename

# Step 3: Merge all PDFs into a single file
def merge_pdfs(pdf_list, output_filename):
    merger = PdfMerger()

    # Append each individual PDF to the merger
    for pdf in pdf_list:
        merger.append(pdf)
    
    # Write the merged PDF to the output file
    merger.write(output_filename)
    merger.close()

# Main Program
def main():
    input_csv = "orders.csv"  # Input CSV file
    output_dir = "invoices"   # Directory to save individual PDFs
    merged_pdf = "All_Invoices.pdf"  # Output merged PDF file
    
    # Create directory for invoices if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load order data from CSV
    order_data = load_order_data(input_csv)
    
    # Generate PDFs and store file paths
    pdf_files = []
    for _, order in order_data.iterrows():
        pdf_file = generate_pdf_invoice(order, output_dir)
        pdf_files.append(pdf_file)
    
    # Merge all PDFs into one file
    merge_pdfs(pdf_files, merged_pdf)
    print(f"All invoices merged into {merged_pdf}")

if __name__ == "__main__":
    main()
