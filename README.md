# Retail Sales Analytics – End-to-End Data Pipeline

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Introduction

This project presents a complete end-to-end analytics pipeline built using **Python**, **SQL**, and **Power BI** — starting from raw transactional data and concluding with a fully interactive dashboard.

The primary objective was to analyze **customer purchasing behavior**, **overall sales performance**, and **product return trends** by combining structured data processing with business-focused visualization.

---

## Why These Tools?

- **Python** – Used for data extraction, preprocessing, and feature engineering  
- **SQL** – Used to structure, query, and prepare analytical datasets  
- **Power BI** – Used to build an interactive dashboard and present actionable insights  

Although Power BI provides built-in transformation capabilities, Python and SQL were intentionally integrated within a Jupyter environment to simulate a realistic analytics workflow. This approach demonstrates how multiple tools operate together in a modular and scalable data pipeline.

---

## Dataset

This project uses the **Online Retail dataset** from the UCI Machine Learning Repository.

The dataset consists of a single Excel file containing two sheets:

- Year 2009–2010  
- Year 2010–2011  

Both sheets were merged, cleaned, and processed using Python. The cleaned dataset was then queried using SQL, and the resulting analytical tables were used to build the final Power BI dashboard.

### Sample Dataset View

![Product Analysis](images/product_analysis_dashboard.jpeg)

# Part 1: ETL & Data Cleaning with Python
``` python
## Part 1: ETL & Data Cleaning with Python
```python
import pandas as pd
import sqlite3

# Load Excel sheets
data_2009 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2009-2010")
data_2010 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")

# Merge datasets
retail_df = pd.concat([data_2009, data_2010], ignore_index=True)

# -------------------- DATA CLEANING --------------------

# Remove missing values
retail_df = retail_df.dropna().copy()

# Remove duplicate records
retail_df = retail_df.drop_duplicates().copy()

# Convert date column to datetime format
retail_df["InvoiceDate"] = pd.to_datetime(
    retail_df["InvoiceDate"],
    errors="coerce"
)

# Extract date components
retail_df["Year"] = retail_df["InvoiceDate"].dt.year
retail_df["Month"] = retail_df["InvoiceDate"].dt.month
retail_df["DayOfWeek"] = retail_df["InvoiceDate"].dt.day_name()
retail_df["Week"] = retail_df["InvoiceDate"].dt.isocalendar().week
retail_df["Quarter"] = retail_df["InvoiceDate"].dt.quarter

# Ensure Customer ID is integer
retail_df["Customer ID"] = retail_df["Customer ID"].astype(int)

# Standardize column names for SQL compatibility
retail_df.columns = (
    retail_df.columns
        .str.lower()
        .str.replace(" ", "_")
)

# Save cleaned dataset to SQLite
connection = sqlite3.connect("online_retail_clean.db")
retail_df.to_sql(
    name="retail_data",
    con=connection,
    index=False,
    if_exists="replace"
)
connection.close()
```
**Overview of the steps:**

- Loading the raw CSV (both sheets)
- Combining sheets
- Handling missing values and duplicates
- Creating new date-based columns
- Renaming columns for SQL compatibility
- Saving the cleaned dataset to a local SQLite database

---

## Part 2: SQL Analysis in Python Script Environment
``` python
import sqlite3
import pandas as pd

connection = sqlite3.connect("online_retail_clean.db")

# Sales summary
sales_query = """
SELECT
    customer_id,
    invoice,
    description,
    country,
    year,
    month,
    week,
    price,
    quantity AS total_quantity,
    quantity * price AS total_revenue,
    invoicedate
FROM retail_data
WHERE quantity > 0
"""

sales_summary = pd.read_sql_query(sales_query, connection)

# Product performance
product_query = """
SELECT
    invoice,
    stockcode,
    description,
    quantity AS total_quantity
FROM retail_data
WHERE quantity > 0
ORDER BY total_quantity DESC
"""

products_by_quantity = pd.read_sql_query(product_query, connection)

# Customer activity
customer_query = """
SELECT
    customer_id,
    invoice,
    quantity * price AS total_spent,
    MAX(invoicedate) AS last_purchase_date,
    COUNT(DISTINCT year || '-' || month) AS active_months
FROM retail_data
GROUP BY customer_id
ORDER BY total_spent DESC
"""

customer_activity = pd.read_sql_query(customer_query, connection)

# Returns analysis
returns_query = """
SELECT
    customer_id,
    invoice,
    country,
    year,
    month,
    week,
    stockcode,
    description,
    price,
    quantity AS total_returns_quantity,
    quantity * price AS total_returns_value,
    invoicedate
FROM retail_data
WHERE quantity < 0
"""

returns_summary = pd.read_sql_query(returns_query, connection)

connection.close()

# Export datasets for Power BI
sales_summary.to_csv("sales_summary.csv", index=False)
products_by_quantity.to_csv("products_by_quantity.csv", index=False)
customer_activity.to_csv("customer_activity.csv", index=False)
returns_summary.to_csv("returns_summary.csv", index=False)
```
**Overview of SQL queries and exports:**

- `sales_summary`: Clean sales transactions and revenue calculations  
- `products_by_quantity`: Products overview (excluding returns) 
- `customer_activity`: Lifetime value and engagement by customer  
- `returns_summary`: Product return patterns and total return values  

All queries are executed using `sqlite3` and exported to CSV for use in Power BI.

---

## Dashboard (Power BI)
### Dashboard Theme Rationale
To provide flexibility and enhance user experience, I’ve designed **two versions of the dashboard** using Power BI: one in a **light theme**, and one in a **dark theme**.

I genuinely like both — and I believe each has its own strengths, depending on the **audience**, the **context**, or even the **time of day** they’re being used.

![thumbnail](https://github.com/user-attachments/assets/29d6cfba-f979-4120-87cf-a49556f1c655)

- **Light Version**  
  Ideal for executive presentations, printed reports, and daytime reviews.  
  It offers a clean, minimal aesthetic that works well for clarity and formal communication.

- **Dark Version**  
  Designed with modern usability in mind — great for internal teams, large display screens, or evening usage.  
  It enhances contrast and helps data patterns pop visually.

By presenting both, the goal is to give users the option to choose the experience that best fits their needs — whether it’s clarity in the boardroom or focus during deep-dive analytics.

The Power BI dashboard brings together insights generated in the previous steps and provides an interactive view into sales trends, customer behavior, and returns.

---

