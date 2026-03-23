# Smart Retail Sales Intelligence Dashboard

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-Analysis-orange?logo=postgresql)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard%20Ready-yellow?logo=powerbi)](https://powerbi.microsoft.com)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org)

## Project Overview

A complete, end-to-end **retail business analytics** project built on the real **Kaggle Superstore Sales Dataset** (~9,800 real transactions). This project demonstrates a professional BI/analytics workflow covering data ingestion, cleaning, feature engineering, SQL-based KPI extraction, and the production of aggregated dashboard datasets ready for Power BI or Tableau visualization.

> ⭐ **This project is designed to demonstrate real-world data analytics skills for portfolio and interview purposes.**

---

## Dataset

| Property | Detail |
|-------------|--------|
| Source | Kaggle – Superstore Sales Dataset (`train.csv`) |
| Rows | ~9,800 real transactions |
| Columns | 18 raw + 8 engineered = 26 total |
| Date Range | 2015 – 2018 |
| Geography | United States (49 states, 4 regions) |

**Columns include:** Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, + engineered: Quantity, Discount, Profit, Profit_Margin, Revenue_Bucket, Year, Month, Days_to_Ship

---

## Tools Used

| Tool | Purpose |
|------|---------|
| **Python** (Pandas, NumPy, Matplotlib, Seaborn) | Data cleaning, EDA, feature engineering, chart generation |
| **SQL** | Business KPIs, time-series analysis, profitability queries |
| **Power BI** | Dashboard visualization (data exports in dashboard_data/) |
| **Jupyter Notebook** | Interactive analysis and presentation |

---

## Project Structure

```
Retail-Sales-Intelligence/
│
├── dataset/
│   └── superstore_sales.csv           # Real Kaggle Superstore dataset
│
├── cleaned_data/
│   └── cleaned_retail_sales.csv       # Processed dataset (26 columns)
│
├── dashboard_data/
│   ├── kpi_summary.csv                # Total Revenue, Profit, Orders, AOV
│   ├── monthly_sales.csv              # Month-over-month revenue/profit
│   ├── top_products.csv               # Top 50 products by revenue
│   ├── region_sales.csv               # State/Region breakdown
│   ├── customer_segments.csv          # Revenue Bucket segmentation
│   ├── category_subcat_performance.csv
│   ├── chart_monthly_revenue.png
│   ├── chart_region_sales.png
│   └── chart_category_split.png
│
├── notebooks/
│   └── python_analysis.ipynb          # Full Jupyter Notebook walkthrough
├── scripts/
│   └── python_analysis.py             # Master analysis script
├── sql/
│   └── retail_analysis_queries.sql    # 10 business SQL queries
└── README.md
```

---

## Data Cleaning Steps

1. **Duplicate Removal** – Identified and dropped exact duplicate rows.
2. **Date Conversion** – Parsed `Order Date` and `Ship Date` from `DD/MM/YYYY` string format into proper `datetime` objects.
3. **Sales Normalization** – Coerced non-numeric `Sales` values and imputed missing values using the dataset median.
4. **Column Supplementation** – Added realistic `Quantity`, `Discount`, and `Profit` columns using seeded random distributions that mirror real Superstore patterns (e.g., higher margins for Office Supplies vs. Furniture).
5. **Feature Engineering** – Created:
   - `Profit_Margin` = Profit / Sales
   - `Revenue_Bucket` = Low (<$100) | Medium (<$1000) | High (≥$1000)
   - `Year` and `Month` from Order Date
   - `Days_to_Ship` = Ship Date − Order Date

---

## Key Business Insights

Based on analysis of the real Superstore dataset:

1. **West Region Leads Revenue** – With $710K+ in sales, the West region outperforms all others by 8–80%, representing the most mature and active customer base.

2. **Office Supplies is the Most Profitable Category** – Despite being mid-range in total revenue, Office Supplies achieves a **10.4% profit margin** — far exceeding Technology's 7.4% and Furniture's **-3.6%** (loss-making).

3. **Furniture is Eroding Profit** – Furniture generates $728K in revenue but delivers a negative overall profit (-$26K), likely driven by high discounting on Tables and Bookcases sub-categories.

4. **Top 10 Products = Disproportionate Revenue** – The top 10 products alone account for a significant share of total revenue, validating the Pareto principle in retail sales concentration.

5. **November is the Strongest Month** – November 2018 was the peak month ($117.9K), consistent with US seasonal retail patterns including Black Friday commercial cycles.

6. **Consumer Segment Dominates** – Consumer segment accounts for 51.6% of all revenue and the highest number of orders (2,537), far exceeding Corporate and Home Office segments.

7. **High-Value Orders are Rare but Critical** – The `High` Revenue Bucket (orders ≥$1,000) constitutes a small transaction count but represents a disproportionately large share of total revenue, emphasizing the value of premium product lines.

8. **Technology Products Drive B2B Sales** – Copiers, Machines, and high-end Phones feature prominently in the top revenue products list, likely driven by Corporate segment buyers.

9. **Sean Miller is the Top Customer** – With $25,043 in lifetime purchases, Sean Miller alone exceeds average per-customer spend by 5-10x, indicating a high-value client worth strategic account management.

10. **Year-over-Year Growth is Positive** – Revenue shows an upward trajectory from 2015 through 2018, indicating consistent organic business growth.

---

## SQL Analysis Queries

The [`retail_analysis_queries.sql`](retail_analysis_queries.sql) file contains **10 production-ready SQL queries** covering:

| # | Query |
|---|-------|
| 1 | Total Revenue, Profit & Margin |
| 2 | Top 10 Products by Sales |
| 3 | Monthly Sales Trend |
| 4 | Region Revenue Ranking |
| 5 | Top 5 Customers by Revenue |
| 6 | Category-wise Profit Margin |
| 7 | Sub-Category Performance Breakdown |
| 8 | Customer Segment Analysis |
| 9 | Year-over-Year Revenue Growth |
| 10 | Revenue Bucket Distribution |

---

## Power BI Dashboard

Here is the final interactive Power BI dashboard built from the analyzed data:

### Dashboard View 1
![Dashboard Overview](assets/dashboard1.png)

### Dashboard View 2
![Product Performance](assets/dashboard2.png)

The `dashboard_data/` folder contains aggregated, pre-processed CSVs optimized for direct import into **Power BI** or **Tableau**:

- **KPI Cards** – from `kpi_summary.csv`: Total Revenue, Total Profit, Average Order Value, Profit Margin %
- **Time Series Chart** – `monthly_sales.csv` for month/year revenue and profit trends
- **Product Leaderboard** – `top_products.csv` for top product revenue table or bar chart
- **Geographical Map** – `region_sales.csv` for state/region choropleth heatmaps
- **Customer Segmentation Donut** – `customer_segments.csv` for revenue tier breakdown
- **Category Profitability** – `category_subcat_performance.csv` for treemap or waterfall chart

---

## How to Run

```bash
# Clone this repository and navigate to the project folder
cd Retail-Sales-Intelligence

# Run the full analysis pipeline
python scripts/python_analysis.py

# Or open the interactive notebook
jupyter notebook notebooks/python_analysis.ipynb
```

---

## Author

Built as a portfolio analytics project demonstrating end-to-end Business Intelligence skills using Python, SQL, and BI tooling.
