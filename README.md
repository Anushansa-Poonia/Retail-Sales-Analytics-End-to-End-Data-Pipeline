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

> **Note:** Raw dataset files are not included due to file size limitations.

---

# Part 1: ETL & Data Cleaning with Python

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
