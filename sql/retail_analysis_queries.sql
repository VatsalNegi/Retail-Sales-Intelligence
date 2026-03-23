-- Smart Retail Sales Intelligence Dashboard
-- SQL Analysis Queries
-- Dataset: Kaggle Superstore Sales | Table: sales_data

-- ============================================================
-- 1. Total Revenue and Total Profit
-- ============================================================
SELECT
    ROUND(SUM(Sales), 2)  AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM sales_data;

-- ============================================================
-- 2. Top 10 Products by Sales
-- ============================================================
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2)  AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(*) AS Num_Orders
FROM sales_data
GROUP BY "Product Name"
ORDER BY Total_Sales DESC
LIMIT 10;

-- ============================================================
-- 3. Monthly Sales Trend
-- ============================================================
SELECT
    Year,
    Month,
    ROUND(SUM(Sales), 2)  AS Monthly_Revenue,
    ROUND(SUM(Profit), 2) AS Monthly_Profit,
    COUNT(DISTINCT "Order ID") AS Orders
FROM sales_data
GROUP BY Year, Month
ORDER BY Year, Month;

-- ============================================================
-- 4. Region with Highest Revenue
-- ============================================================
SELECT
    Region,
    ROUND(SUM(Sales), 2)  AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(DISTINCT "Order ID") AS Total_Orders
FROM sales_data
GROUP BY Region
ORDER BY Total_Revenue DESC;

-- ============================================================
-- 5. Top 5 Customers by Revenue
-- ============================================================
SELECT
    "Customer Name",
    "Customer ID",
    Segment,
    Region,
    ROUND(SUM(Sales), 2)  AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(DISTINCT "Order ID") AS Total_Orders
FROM sales_data
GROUP BY "Customer Name", "Customer ID", Segment, Region
ORDER BY Total_Revenue DESC
LIMIT 5;

-- ============================================================
-- 6. Category-wise Profit Margin
-- ============================================================
SELECT
    Category,
    ROUND(SUM(Sales), 2)  AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Category
ORDER BY Profit_Margin_Pct DESC;

-- ============================================================
-- 7. Sub-Category Performance (bonus insight)
-- ============================================================
SELECT
    Category,
    "Sub-Category",
    ROUND(SUM(Sales), 2)  AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Category, "Sub-Category"
ORDER BY Profit_Margin_Pct DESC;

-- ============================================================
-- 8. Customer Segment Analysis
-- ============================================================
SELECT
    Segment,
    COUNT(DISTINCT "Customer ID") AS Num_Customers,
    ROUND(SUM(Sales), 2)          AS Total_Revenue,
    ROUND(AVG(Sales), 2)          AS Avg_Order_Value,
    ROUND(SUM(Profit), 2)         AS Total_Profit
FROM sales_data
GROUP BY Segment
ORDER BY Total_Revenue DESC;

-- ============================================================
-- 9. Year-over-Year Revenue Growth
-- ============================================================
SELECT
    Year,
    ROUND(SUM(Sales), 2) AS Annual_Revenue,
    ROUND(SUM(Profit), 2) AS Annual_Profit
FROM sales_data
GROUP BY Year
ORDER BY Year;

-- ============================================================
-- 10. Revenue Bucket Distribution
-- ============================================================
SELECT
    Revenue_Bucket,
    COUNT(*) AS Num_Transactions,
    ROUND(SUM(Sales), 2)  AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales_data
GROUP BY Revenue_Bucket
ORDER BY Total_Revenue DESC;
