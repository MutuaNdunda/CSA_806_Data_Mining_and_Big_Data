#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 09:28:30 2025

@author: mutua
"""

import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker("en_US")  # we'll override names/locations for Kenya context
np.random.seed(42)
random.seed(42)

# -----------------------------
# 1️⃣ Dimension: Customers
# -----------------------------
# Base sample customers
customers = [
    [1001, "John Kamau", "25–34", "Male", "Naivasha", "Nakuru"],
    [1002, "Jane Auma", "35–44", "Female", "Gilgil", "Nakuru"],
    [1003, "Alice Makena", "45–54", "Female", "Chogoria", "Tharaka Nithi"]
]

kenyan_towns = [
    ("Nairobi","Nairobi"), ("Kisumu","Kisumu"), ("Mombasa","Mombasa"),
    ("Eldoret","Uasin Gishu"), ("Nakuru","Nakuru"), ("Meru","Meru"),
    ("Nyeri","Nyeri"), ("Embu","Embu"), ("Machakos","Machakos"),
    ("Thika","Kiambu"), ("Kitale","Trans Nzoia"), ("Kericho","Kericho"),
    ("Naivasha","Nakuru"), ("Gilgil","Nakuru"), ("Chogoria","Tharaka Nithi")
]

age_groups = ["18–24","25–34","35–44","45–54","55–64","65+"]

for cid in range(1004, 1004 + (700 - 3)):
    name = fake.first_name() + " " + fake.last_name()
    age_group = random.choice(age_groups)
    gender = random.choice(["Male","Female"])
    town, county = random.choice(kenyan_towns)
    customers.append([cid, name, age_group, gender, town, county])

customer_df = pd.DataFrame(customers, columns=["CustomerID","Name","AgeGroup","Gender","Town","County"])

# -----------------------------
# 2️⃣ Dimension: Products
# -----------------------------
categories = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Camera"],
    "Furniture": ["Chair", "Table", "Sofa", "Bed"],
    "Grocery": ["Maize Flour","Rice","Sugar","Tea"],
    "Clothing": ["Shirt","Dress","Shoes","Jacket"]
}
brands = ["Brand X","Brand Y","Brand Z","Brand K","Brand M"]

products = [
    [2001, "Laptop A", "Electronics", "Brand X", 500],
    [2002, "Smartphone B", "Electronics", "Brand Y", 300],
    [2003, "Chair C", "Furniture", "Brand Z", 100]
]

pid = 2004
for _ in range(47):  # ~50 total products
    cat = random.choice(list(categories.keys()))
    base_name = random.choice(categories[cat])
    prod_name = f"{base_name} {random.choice(['A','B','C','D','E'])}"
    brand = random.choice(brands)
    price = round(random.uniform(50, 2000), 2)
    products.append([pid, prod_name, cat, brand, price])
    pid += 1

product_df = pd.DataFrame(products, columns=["ProductID","ProductName","Category","Brand","Price"])

# -----------------------------
# 3️⃣ Dimension: Time
# -----------------------------
time_records = []
tid = 1
dates = pd.date_range(start="2024-01-01", end="2025-12-31")
for d in dates:
    time_records.append([
        tid, d.year,
        f"Q{((d.month-1)//3)+1}",
        d.strftime("%B"),
        d.day,
        d.strftime("%A")
    ])
    tid += 1

time_df = pd.DataFrame(time_records, columns=["TimeID","Year","Quarter","Month","Day","Weekday"])

# -----------------------------
# 4️⃣ Dimension: Stores
# -----------------------------
store_list = [
    [101, "Store 1", "Nakuru", "Juma"],
    [102, "Store 2", "Kisumu", "Pamela"],
    [103, "Store 3", "Meru", "Alima"]
]
for sid in range(104, 121):
    town, county = random.choice(kenyan_towns)
    manager = fake.first_name()
    store_list.append([sid, f"Store {sid-100}", town, manager])

store_df = pd.DataFrame(store_list, columns=["StoreID","StoreName","Location","Manager"])

# -----------------------------
# 5️⃣ Fact Table: Sales
# -----------------------------
fact_rows = []
for tidx in range(1, 1001):
    cust_id = random.choice(customer_df["CustomerID"])
    prod_id = random.choice(product_df["ProductID"])
    time_id = random.choice(time_df["TimeID"])
    store_id = random.choice(store_df["StoreID"])
    price = float(product_df.loc[product_df.ProductID == prod_id, "Price"].values[0])
    units = random.randint(1, 10)
    discount = round(random.uniform(0, 0.20), 2)
    revenue = round(price * units * (1 - discount), 2)
    fact_rows.append([tidx, cust_id, prod_id, time_id, store_id, revenue, units, discount])

sales_fact_df = pd.DataFrame(
    fact_rows,
    columns=["TransactionID","CustomerID","ProductID","TimeID","StoreID","Revenue","UnitsSold","Discount"]
)

# -----------------------------
# Save to CSV (optional)
# -----------------------------
customer_df.to_csv("customer_dim.csv", index=False)
product_df.to_csv("product_dim.csv", index=False)
time_df.to_csv("time_dim.csv", index=False)
store_df.to_csv("store_dim.csv", index=False)
sales_fact_df.to_csv("sales_fact.csv", index=False)

# Quick check
print(customer_df.head())
print(product_df.head())
print(time_df.head())
print(store_df.head())
print(sales_fact_df.head())

