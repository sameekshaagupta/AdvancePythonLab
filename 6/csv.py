import os
import pandas as pd
import glob

def read_sales_data(directory):
    all_files = glob.glob(os.path.join(directory, '**', '*.csv'), recursive=True)
    sales_data = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
    return sales_data

def calculate_total_sales(sales_data):
    total_sales = sales_data.groupby('Product ID')['Quantity sold'].sum().reset_index()
    return total_sales

def get_top_5_products(total_sales):
    top_5_products = total_sales.sort_values(by='Quantity sold', ascending=False).head(5)
    return top_5_products

def add_product_names(total_sales, product_names_file):
    product_names = pd.read_csv(product_names_file)
    sales_with_names = total_sales.merge(product_names, on='Product ID', how='left')
    return sales_with_names

def calculate_average_sales_per_month(sales_data, total_sales):
    sales_data['Year-Month'] = sales_data['Date'].str[:7]  # Extract year-month
    unique_months = sales_data['Year-Month'].nunique()
    total_sales['Average Quantity Sold per Month'] = total_sales['Quantity sold'] / unique_months
    return total_sales

def save_sales_summary(sales_summary, output_file):
    sales_summary.to_csv(output_file, index=False, columns=['Product ID', 'Product Name', 'Quantity sold', 'Average Quantity Sold per Month'])

def main(directory, product_names_file, output_file):
    # Step 1: Read all sales data
    sales_data = read_sales_data(directory)
    
    # Step 2: Calculate total sales for each product
    total_sales = calculate_total_sales(sales_data)
    
    # Step 3: Add product names to the sales data
    total_sales_with_names = add_product_names(total_sales, product_names_file)
    
    # Step 4: Calculate average quantity sold per month
    total_sales_with_avg = calculate_average_sales_per_month(sales_data, total_sales_with_names)
    
    # Step 5: Save the summary to a CSV file
    save_sales_summary(total_sales_with_avg, output_file)

# Example usage
main('path/to/sales/data', 'product_names.csv', 'sales_summary.csv')
