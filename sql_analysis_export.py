import sqlite3
import pandas as pd

connection = sqlite3.connect("online_retail_clean.db")

# -------------------- SALES SUMMARY --------------------

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

# -------------------- PRODUCTS BY QUANTITY --------------------

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

# -------------------- CUSTOMER ACTIVITY --------------------

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

# -------------------- RETURNS SUMMARY --------------------

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

# Export for Power BI
sales_summary.to_csv("sales_summary.csv", index=False)
products_by_quantity.to_csv("products_by_quantity.csv", index=False)
customer_activity.to_csv("customer_activity.csv", index=False)
returns_summary.to_csv("returns_summary.csv", index=False)
