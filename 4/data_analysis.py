import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# Step 1: Data Loading
df = pd.read_csv('4/data.csv')

# Step 2: Data Cleaning
print("Missing values in each column:\n", df.isnull().sum())
df_cleaned = df.dropna(subset=['CustomerID'])
df_cleaned = df_cleaned.drop_duplicates()
df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'], format='%d/%m/%y %H:%M')

# Calculate Total Amount Spent and Total Items Purchased
df_cleaned['TotalAmountSpent'] = df_cleaned['Quantity'] * df_cleaned['UnitPrice']
df_cleaned['TotalItemsPurchased'] = df_cleaned.groupby('CustomerID')['Quantity'].transform('sum')

# Calculate Average Purchase Value
df_cleaned['AveragePurchaseValue'] = df_cleaned['TotalAmountSpent'] / df_cleaned['TotalItemsPurchased']

# Aggregate features by CustomerID
features = df_cleaned.groupby('CustomerID').agg({
    'TotalAmountSpent': 'sum',
    'TotalItemsPurchased': 'sum',
    'AveragePurchaseValue': 'mean'
}).reset_index()

# Handle missing values in features
features = features.dropna()  # Or use imputer if preferred

# Normalize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features[['TotalAmountSpent', 'TotalItemsPurchased', 'AveragePurchaseValue']])

# Apply K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
features['Segment'] = kmeans.fit_predict(features_scaled)

# Display the first few rows with segments
print(features.head())

# Step 5: Visualization
plt.figure(figsize=(10, 6))
plt.scatter(features['TotalAmountSpent'], features['TotalItemsPurchased'], c=features['Segment'], cmap='viridis')
plt.xlabel('Total Amount Spent')
plt.ylabel('Total Items Purchased')
plt.title('Customer Segmentation')
plt.show()

# Step 6: Customer Insights
segment_insights = features.groupby('Segment').mean()
print(f"Segment Insights:\n{segment_insights}")

# Step 7: Customer Engagement Recommendations
threshold = features['TotalAmountSpent'].mean()
for segment in segment_insights.index:
    if segment_insights.loc[segment, 'TotalAmountSpent'] > threshold:
        print(f"Segment {segment}: High Spenders - Offer loyalty rewards or exclusive discounts.")
    elif segment_insights.loc[segment, 'TotalItemsPurchased'] > threshold:
        print(f"Segment {segment}: Frequent Shoppers - Send personalized product recommendations.")
    else:
        print(f"Segment {segment}: Inactive Customers - Run re-engagement campaigns with special offers.")
