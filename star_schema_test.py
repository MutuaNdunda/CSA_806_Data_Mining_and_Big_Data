#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 09:56:12 2025

@author: mutua
"""

import pandas as pd

# --- Load the CSVs you exported earlier ---
customer_df = pd.read_csv("customer_dim.csv")
product_df  = pd.read_csv("product_dim.csv")
time_df     = pd.read_csv("time_dim.csv")
store_df    = pd.read_csv("store_dim.csv")
sales_fact_df = pd.read_csv("sales_fact.csv")

# --- Helper to check primary key uniqueness ---
def check_primary_key_unique(df, key_name):
    dups = df[key_name].duplicated().sum()
    if dups == 0:
        print(f"✅ {key_name} is unique in {key_name.split('ID')[0]} dimension.")
    else:
        print(f"❌ {key_name} has {dups} duplicate values.")

check_primary_key_unique(customer_df, "CustomerID")
check_primary_key_unique(product_df,  "ProductID")
check_primary_key_unique(time_df,     "TimeID")
check_primary_key_unique(store_df,    "StoreID")

# --- Helper to check FK→PK relationship ---
def check_foreign_key(fact_df, fact_col, dim_df, dim_col):
    missing = fact_df.loc[~fact_df[fact_col].isin(dim_df[dim_col])]
    if missing.empty:
        print(f"✅ All {fact_col} values in fact table exist in {dim_col} of dimension table.")
    else:
        print(f"❌ {len(missing)} {fact_col} values in fact table have no match in dimension table.")
        print(missing[[fact_col]].drop_duplicates())

check_foreign_key(sales_fact_df, "CustomerID", customer_df, "CustomerID")
check_foreign_key(sales_fact_df, "ProductID",  product_df,  "ProductID")
check_foreign_key(sales_fact_df, "TimeID",     time_df,     "TimeID")
check_foreign_key(sales_fact_df, "StoreID",    store_df,    "StoreID")

# --- Optional sanity checks ---
print("\nSummary:")
print("Fact table rows:", len(sales_fact_df))
print("Distinct customers in fact:", sales_fact_df['CustomerID'].nunique())
print("Distinct products in fact:",  sales_fact_df['ProductID'].nunique())
print("Distinct stores in fact:",    sales_fact_df['StoreID'].nunique())
print("Distinct time IDs in fact:",  sales_fact_df['TimeID'].nunique())
