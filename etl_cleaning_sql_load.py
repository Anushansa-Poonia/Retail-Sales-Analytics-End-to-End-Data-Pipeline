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

# Make column names SQL-friendly
retail_df.columns = (
    retail_df.columns
        .str.lower()
        .str.replace(" ", "_")
)

# -------------------- SAVE TO SQLITE --------------------

connection = sqlite3.connect("online_retail_clean.db")
retail_df.to_sql(
    name="retail_data",
    con=connection,
    index=False,
    if_exists="replace"
)
connection.close()
