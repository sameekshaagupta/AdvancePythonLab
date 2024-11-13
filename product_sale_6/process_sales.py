import os
import pandas as pd

def process_sales_data(sales_dir, product_mapping_file, output_file):
    # Load product mapping file
    product_mapping = pd.read_csv(product_mapping_file)
    product_dict = product_mapping.set_index('Product ID')['Product Name'].to_dict()

    # Initialize an empty DataFrame to combine all sales data
    all_sales_data = pd.DataFrame()

    # Traverse all files in the sales directory
    for root, _, files in os.walk(sales_dir):
        for file in files:
            if file.endswith(".csv") and file != os.path.basename(product_mapping_file):
                filepath = os.path.join(root, file)
                sales_data = pd.read_csv(filepath)
                all_sales_data = pd.concat([all_sales_data, sales_data], ignore_index=True)

    # Ensure the Date column is datetime type
    all_sales_data['Date'] = pd.to_datetime(all_sales_data['Date'])
    all_sales_data['Month-Year'] = all_sales_data['Date'].dt.to_period('M')

    # Group by Product ID and calculate total and average quantities
    total_sales = all_sales_data.groupby('Product ID')['Quantity sold'].sum()
    months = all_sales_data['Month-Year'].nunique()
    avg_sales = total_sales / months

    # Combine results into a DataFrame
    summary_df = pd.DataFrame({
        "Product ID": total_sales.index,
        "Product Name": total_sales.index.map(product_dict),
        "Total Quantity Sold": total_sales.values,
        "Average Quantity Sold per Month": avg_sales.values
    })

    # Sort by total sales and keep top 5
    summary_df = summary_df.sort_values(by="Total Quantity Sold", ascending=False).head(5)

    # Write to CSV
    summary_df.to_csv(output_file, index=False)
    print(f"Sales summary saved to {output_file}")

# Define paths
sales_directory = "./sales_data"
product_mapping_file = "./product_names.csv"
output_file = "sales_summary.csv"

# Run the function
process_sales_data(sales_directory, product_mapping_file, output_file)
