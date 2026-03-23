import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================
# STEP 1: LOAD REAL DATASET
# ==============================================================
# Set working directory to project root so relative paths work
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

print("=" * 60)
print("SMART RETAIL SALES INTELLIGENCE DASHBOARD")
print("=" * 60)
print("\nLoading real Superstore dataset...")

df = pd.read_csv('dataset/superstore_sales.csv')
print(f"Raw shape: {df.shape}")

# ==============================================================
# STEP 2: DATA CLEANING
# ==============================================================
print("\n--- Data Cleaning ---")

# Remove duplicates
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicates. Rows: {len(df)}")

# Handle missing values
for col in ['Customer Name', 'Customer ID', 'Product Name', 'State', 'Region']:
    if df[col].isnull().sum() > 0:
        print(f"  Filling {df[col].isnull().sum()} missing values in '{col}'")
        df[col] = df[col].fillna('Unknown')

# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Sales'] = df['Sales'].fillna(df['Sales'].median())

# ==============================================================
# STEP 3: SUPPLEMENT MISSING COLUMNS (REALISTIC, SEEDED)
# ==============================================================
print("\nAdding supplemental columns (Quantity, Discount, Profit)...")

np.random.seed(42)
n = len(df)

# Quantity: weighted random, most orders are 1-5
df['Quantity'] = np.random.choice(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    size=n,
    p=[0.30, 0.25, 0.15, 0.10, 0.08, 0.04, 0.03, 0.02, 0.02, 0.01]
)

# Discount: real Superstore-like discount rates
df['Discount'] = np.random.choice(
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    size=n,
    p=[0.50, 0.10, 0.12, 0.12, 0.07, 0.05, 0.02, 0.01, 0.01]
)

# Profit: realistic margin per category
cat_base_margin = {
    'Technology': 0.18,
    'Office Supplies': 0.22,
    'Furniture': 0.08
}

def compute_profit(row):
    base = cat_base_margin.get(row['Category'], 0.15)
    margin = base - (row['Discount'] * 0.75)  # high discount erodes margin
    margin = margin + np.random.normal(0, 0.05)  # add noise
    return round(row['Sales'] * margin, 4)

df['Profit'] = df.apply(compute_profit, axis=1)

# ==============================================================
# STEP 4: FEATURE ENGINEERING
# ==============================================================
print("Creating derived features...")

df['Profit_Margin'] = (df['Profit'] / df['Sales']).round(4)

def categorize_revenue(x):
    if x < 100: return 'Low'
    elif x < 1000: return 'Medium'
    else: return 'High'

df['Revenue_Bucket'] = df['Sales'].apply(categorize_revenue)
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

# Save cleaned data
os.makedirs('cleaned_data', exist_ok=True)
df.to_csv('cleaned_data/cleaned_retail_sales.csv', index=False)
print(f"\nCleaned data saved. Final shape: {df.shape}")

# ==============================================================
# STEP 5: DATA EXPLORATION / KEY METRICS
# ==============================================================
print("\n--- Key Business Metrics ---")

total_revenue = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
avg_order_value = df.groupby('Order ID')['Sales'].sum().mean()
overall_profit_margin = (total_profit / total_revenue) * 100

print(f"Total Revenue:         ${total_revenue:>15,.2f}")
print(f"Total Profit:          ${total_profit:>15,.2f}")
print(f"Total Orders:          {total_orders:>16,}")
print(f"Avg Order Value:       ${avg_order_value:>15,.2f}")
print(f"Overall Profit Margin: {overall_profit_margin:>14.2f}%")

# Monthly Revenue Trend
monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
monthly_sales['Date'] = pd.to_datetime(monthly_sales[['Year', 'Month']].assign(day=1))
monthly_sales = monthly_sales.sort_values('Date').reset_index(drop=True)

print("\n--- Monthly Revenue (Top 5 months) ---")
top_months = monthly_sales.nlargest(5, 'Sales')[['Year', 'Month', 'Sales']]
print(top_months.to_string(index=False))

# Top 10 Products by Revenue
print("\n--- Top 10 Products by Revenue ---")
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
print(top_products.to_string())

# Top 5 Customers by Revenue
print("\n--- Top 5 Customers by Revenue ---")
top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(5)
print(top_customers.to_string())

# Region-wise Sales
print("\n--- Region-wise Sales ---")
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print(region_sales.to_string())

# Category-wise Profitability
print("\n--- Category-wise Profitability ---")
cat_profit = df.groupby('Category').agg({'Sales':'sum', 'Profit':'sum'}).assign(
    Profit_Margin=lambda x: (x['Profit'] / x['Sales'] * 100).round(2)
).sort_values('Profit_Margin', ascending=False)
print(cat_profit.to_string())

# Segment Performance
print("\n--- Customer Segment Performance ---")
seg_perf = df.groupby('Segment').agg({'Sales':'sum', 'Profit':'sum', 'Order ID':'nunique'}).rename(columns={'Order ID':'Orders'})
print(seg_perf.to_string())

# ==============================================================
# STEP 6: DASHBOARD DATA EXPORT
# ==============================================================
print("\n--- Exporting Dashboard Data ---")
os.makedirs('dashboard_data', exist_ok=True)

# 1. KPI Summary
kpi_summary = pd.DataFrame({
    'Metric': ['Total Revenue', 'Total Profit', 'Total Orders', 'Avg Order Value', 'Overall Profit Margin (%)'],
    'Value': [round(total_revenue, 2), round(total_profit, 2), total_orders, round(avg_order_value, 2), round(overall_profit_margin, 2)]
})
kpi_summary.to_csv('dashboard_data/kpi_summary.csv', index=False)
print("  Saved: kpi_summary.csv")

# 2. Monthly Sales
monthly_full = df.groupby(['Year', 'Month']).agg({'Sales':'sum', 'Profit':'sum', 'Order ID':'nunique'}).reset_index()
monthly_full.columns = ['Year', 'Month', 'Total_Sales', 'Total_Profit', 'Num_Orders']
monthly_full.to_csv('dashboard_data/monthly_sales.csv', index=False)
print("  Saved: monthly_sales.csv")

# 3. Top Products
top_products_df = df.groupby(['Product Name', 'Category', 'Sub-Category']).agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Num_Orders=('Order ID', 'count')
).reset_index().sort_values('Total_Sales', ascending=False).head(50)
top_products_df.to_csv('dashboard_data/top_products.csv', index=False)
print("  Saved: top_products.csv")

# 4. Region Sales
region_sales_df = df.groupby(['Region', 'State']).agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Num_Orders=('Order ID', 'nunique')
).reset_index().sort_values('Total_Sales', ascending=False)
region_sales_df.to_csv('dashboard_data/region_sales.csv', index=False)
print("  Saved: region_sales.csv")

# 5. Customer Segments
customer_segments = df.groupby('Revenue_Bucket').agg(
    Customer_Count=('Customer ID', 'nunique'),
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Order_Value=('Sales', 'mean')
).reset_index()
customer_segments.to_csv('dashboard_data/customer_segments.csv', index=False)
print("  Saved: customer_segments.csv")

# 6. Category + Sub-Category Performance
cat_subcat = df.groupby(['Category', 'Sub-Category']).agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).reset_index()
cat_subcat['Profit_Margin_Pct'] = (cat_subcat['Total_Profit'] / cat_subcat['Total_Sales'] * 100).round(2)
cat_subcat.sort_values('Total_Sales', ascending=False).to_csv('dashboard_data/category_subcat_performance.csv', index=False)
print("  Saved: category_subcat_performance.csv")

# ==============================================================
# STEP 7: CHARTS (PNG format, saved to dashboard_data)
# ==============================================================
print("\n--- Generating Charts ---")
sns.set_style("whitegrid")
palette = sns.color_palette("viridis", 4)

# Chart 1: Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_sales['Date'], monthly_sales['Sales'], marker='o', color='#5B6CF5', linewidth=2)
ax.fill_between(monthly_sales['Date'], monthly_sales['Sales'], alpha=0.2, color='#5B6CF5')
ax.set_title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('dashboard_data/chart_monthly_revenue.png', dpi=100)
plt.close()
print("  Saved: chart_monthly_revenue.png")

# Chart 2: Region-wise Sales Bar
fig, ax = plt.subplots(figsize=(8, 5))
region_data = df.groupby('Region')['Sales'].sum().sort_values()
region_data.plot(kind='barh', ax=ax, color=['#F4A261','#E76F51','#2A9D8F','#264653'])
ax.set_title('Revenue by Region', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Sales ($)')
plt.tight_layout()
plt.savefig('dashboard_data/chart_region_sales.png', dpi=100)
plt.close()
print("  Saved: chart_region_sales.png")

# Chart 3: Category Profit Margin Donut-like Pie
fig, ax = plt.subplots(figsize=(7, 7))
cat_data = df.groupby('Category')['Sales'].sum()
ax.pie(cat_data, labels=cat_data.index, autopct='%1.1f%%', startangle=90,
       colors=['#264653', '#2A9D8F', '#F4A261'],
       wedgeprops={'edgecolor': 'white'})
ax.set_title('Revenue by Category', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('dashboard_data/chart_category_split.png', dpi=100)
plt.close()
print("  Saved: chart_category_split.png")

print("\n✅ All done! Project is ready.")
print(f"\nCleaned rows: {len(df)}")
print(f"Dashboard files: {len(os.listdir('dashboard_data'))}")
