import os
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt

# Load the customer data from CSV file
def load_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found.")
    return pd.read_csv(filename)

# Generate a pie chart showing purchase distribution by age group
def generate_pie_chart(df):
    age_groups = pd.cut(df['Age'], bins=[18, 25, 35, 50, 100], labels=['18-25', '26-35', '36-50', '51+'])
    age_group_counts = age_groups.value_counts()
    age_group_counts.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(6,6))
    plt.title("Purchase Distribution by Age Group")
    plt.ylabel("")
    plt.show()

# Generate a PDF report
def generate_pdf(df, filename="customer_report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Customer Purchase Report", ln=True, align='C')

    # Summary
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)

    # Calculate total, unique customers, and average purchase by age group
    df['Age Group'] = pd.cut(df['Age'], bins=[18, 25, 35, 50, 100], labels=['18-25', '26-35', '36-50', '51+'])
    summary = df.groupby('Age Group').agg(
        Total_Purchase=('Purchase Amount', 'sum'),
        Unique_Customers=('Customer ID', 'nunique'),
        Avg_Purchase=('Purchase Amount', 'mean')
    )

    # Display summary in table
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 10, 'Age Group')
    pdf.cell(40, 10, 'Total Purchase')
    pdf.cell(40, 10, 'Unique Customers')
    pdf.cell(40, 10, 'Avg Purchase')
    pdf.ln(10)
    
    for index, row in summary.iterrows():
        pdf.cell(40, 10, index)
        pdf.cell(40, 10, f"${row['Total_Purchase']:.2f}")
        pdf.cell(40, 10, str(row['Unique_Customers']))
        pdf.cell(40, 10, f"${row['Avg_Purchase']:.2f}")
        pdf.ln(5)

    pdf.output(filename)

# Main function to execute the script
def main():
    try:
        # Load customer data
        df = load_data('customer_data.csv')

        # Generate pie chart
        generate_pie_chart(df)

        # Generate PDF report
        generate_pdf(df)
        print("Report generated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
