import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Step 1: Data Loading
# Load the dataset
df = pd.read_csv('4\\Online Retail.xlsx')

# Display the first few rows
print(df.head())

# Step 2: Data Cleaning
# Check for missing values
print("Missing values in each column:\n", df.isnull().sum())

# Drop rows with missing CustomerID
df_cleaned = df.dropna(subset=['CustomerID'])

# Drop duplicates
df_cleaned = df_cleaned.drop_duplicates()

# Convert InvoiceDate to datetime format
df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])

# Step 3: Descriptive Statistics
# Calculate Total Amount Spent and Total Items Purchased
df_cleaned['TotalAmountSpent'] = df_cleaned['Quantity'] * df_cleaned['UnitPrice']
df_cleaned['TotalItemsPurchased'] = df_cleaned.groupby('CustomerID')['Quantity'].transform('sum')

# Calculate descriptive statistics
total_spent_stats = df_cleaned['TotalAmountSpent'].describe()
total_items_stats = df_cleaned['TotalItemsPurchased'].describe()

print(f"Total Amount Spent Stats:\n{total_spent_stats}")
print(f"Total Items Purchased Stats:\n{total_items_stats}")

# Step 4: Customer Segmentation
# Calculate Average Purchase Value
df_cleaned['AveragePurchaseValue'] = df_cleaned['TotalAmountSpent'] / df_cleaned['TotalItemsPurchased']

# Select relevant features for clustering
features = df_cleaned.groupby('CustomerID').agg({
    'TotalAmountSpent': 'sum',
    'TotalItemsPurchased': 'sum',
    'AveragePurchaseValue': 'mean'
}).reset_index()

# Normalize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features[['TotalAmountSpent', 'TotalItemsPurchased', 'AveragePurchaseValue']])

# Apply K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
features['Segment'] = kmeans.fit_predict(features_scaled)

# Display the first few rows with segments
print(features.head())

# Step 5: Visualization
# Scatter plot of Total Amount Spent vs. Total Items Purchased, colored by segment
plt.figure(figsize=(10, 6))
plt.scatter(features['TotalAmountSpent'], features['TotalItemsPurchased'], c=features['Segment'], cmap='viridis')
plt.xlabel('Total Amount Spent')
plt.ylabel('Total Items Purchased')
plt.title('Customer Segmentation')
plt.show()

# Step 6: Customer Insights
# Group by segments and calculate mean values for each segment
segment_insights = features.groupby('Segment').mean()

print(f"Segment Insights:\n{segment_insights}")

# Step 7: Customer Engagement Recommendations
threshold = features['TotalAmountSpent'].mean()  # Example threshold for high spenders

for segment in segment_insights.index:
    if segment_insights.loc[segment, 'TotalAmountSpent'] > threshold:
        print(f"Segment {segment}: High Spenders - Offer loyalty rewards or exclusive discounts.")
    elif segment_insights.loc[segment, 'TotalItemsPurchased'] > threshold:
        print(f"Segment {segment}: Frequent Shoppers - Send personalized product recommendations.")
    else:
        print(f"Segment {segment}: Inactive Customers - Run re-engagement campaigns with special offers.")
