#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 10:46:47 2025

@author: mutua
"""
"""
Created on Tue Sep 23 09:28:30 2025
@author: mutua
Generates a Snowflake-style schema dataset for a Kenyan retail sales scenario.
"""

import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker("en_US")
np.random.seed(42)
random.seed(42)

# -----------------------------
# Lookup Tables (1st normal form)
# -----------------------------
age_groups = ["18–24","25–34","35–44","45–54","55–64","65+"]
gender_list = ["Male","Female"]

counties = [
    "Nairobi","Nakuru","Kisumu","Mombasa","Uasin Gishu","Meru",
    "Nyeri","Embu","Machakos","Kiambu","Trans Nzoia","Kericho","Tharaka Nithi"
]

towns = [
    ("Nairobi","Nairobi"),("Kisumu","Kisumu"),("Mombasa","Mombasa"),
    ("Eldoret","Uasin Gishu"),("Nakuru","Nakuru"),("Meru","Meru"),
    ("Nyeri","Nyeri"),("Embu","Embu"),("Machakos","Machakos"),
    ("Thika","Kiambu"),("Kitale","Trans Nzoia"),("Kericho","Kericho"),
    ("Naivasha","Nakuru"),("Gilgil","Nakuru"),("Chogoria","Tharaka Nithi")
]

categories = ["Electronics","Furniture","Grocery","Clothing"]
brands = ["Brand X","Brand Y","Brand Z","Brand K","Brand M"]

quarters = [("Q1","Q1"),("Q2","Q2"),("Q3","Q3"),("Q4","Q4")]
months = [(i, pd.Timestamp(year=2024, month=i, day=1).strftime("%B")) for i in range(1,13)]

managers = [fake.first_name() for _ in range(30)]

# Build lookup DataFrames with surrogate keys
age_group_df = pd.DataFrame({"AgeGroupID":range(1,len(age_groups)+1),"AgeGroupName":age_groups})
gender_df    = pd.DataFrame({"GenderID":range(1,len(gender_list)+1),"GenderName":gender_list})
county_df    = pd.DataFrame({"CountyID":range(1,len(counties)+1),"CountyName":counties})
town_df      = pd.DataFrame({
    "TownID": range(1,len(towns)+1),
    "TownName":[t[0] for t in towns],
    "CountyID":[counties.index(t[1])+1 for t in towns]
})
category_df  = pd.DataFrame({"CategoryID":range(1,len(categories)+1),"CategoryName":categories})
brand_df     = pd.DataFrame({"BrandID":range(1,len(brands)+1),"BrandName":brands})
quarter_df   = pd.DataFrame({"QuarterID":range(1,5),"QuarterName":["Q1","Q2","Q3","Q4"]})
month_df     = pd.DataFrame({"MonthID":[m[0] for m in months],"MonthName":[m[1] for m in months]})
manager_df   = pd.DataFrame({"ManagerID":range(1,len(managers)+1),"ManagerName":managers})

# -----------------------------
# Dimension: Customers
# -----------------------------
customers = [
    [1001, "John Kamau", 2, 1, towns.index(("Naivasha","Nakuru"))+1],
    [1002, "Jane Auma", 3, 2, towns.index(("Gilgil","Nakuru"))+1],
    [1003, "Alice Makena", 4, 2, towns.index(("Chogoria","Tharaka Nithi"))+1]
]

for cid in range(1004, 1004 + (700 - 3)):
    name = fake.first_name() + " " + fake.last_name()
    age_id = random.randint(1, len(age_groups))
    gender_id = random.randint(1, len(gender_list))
    town_id = random.randint(1, len(towns))
    customers.append([cid, name, age_id, gender_id, town_id])

customer_df = pd.DataFrame(customers,
    columns=["CustomerID","CustomerName","AgeGroupID","GenderID","TownID"])

# -----------------------------
# Dimension: Products
# -----------------------------
products = [
    [2001, "Laptop A", 1, 1, 500],
    [2002, "Smartphone B", 1, 2, 300],
    [2003, "Chair C", 2, 3, 100]
]

pid = 2004
for _ in range(47):
    cat_id = random.randint(1,len(categories))
    brand_id = random.randint(1,len(brands))
    base_name = random.choice(["Laptop","Smartphone","Tablet","Camera","Chair","Table","Sofa","Bed",
                               "Maize Flour","Rice","Sugar","Tea","Shirt","Dress","Shoes","Jacket"])
    prod_name = f"{base_name} {random.choice(['A','B','C','D'])}"
    price = round(random.uniform(50,2000),2)
    products.append([pid, prod_name, cat_id, brand_id, price])
    pid += 1

product_df = pd.DataFrame(products,
    columns=["ProductID","ProductName","CategoryID","BrandID","Price"])

# -----------------------------
# Dimension: Time
# -----------------------------
time_records = []
tid = 1
for d in pd.date_range("2024-01-01","2025-12-31"):
    q_id = ((d.month-1)//3)+1
    m_id = d.month
    time_records.append([tid, d.year, q_id, m_id, d.day, d.strftime("%A")])
    tid += 1

time_df = pd.DataFrame(time_records,
    columns=["TimeID","Year","QuarterID","MonthID","Day","Weekday"])

# -----------------------------
# Dimension: Stores
# -----------------------------
store_rows = [
    [101,"Store 1",towns.index(("Nakuru","Nakuru"))+1,1],
    [102,"Store 2",towns.index(("Kisumu","Kisumu"))+1,2],
    [103,"Store 3",towns.index(("Meru","Meru"))+1,3]
]
for sid in range(104,121):
    town_id = random.randint(1,len(towns))
    mgr_id = random.randint(1,len(managers))
    store_rows.append([sid,f"Store {sid-100}",town_id,mgr_id])

store_df = pd.DataFrame(store_rows,
    columns=["StoreID","StoreName","TownID","ManagerID"])

# -----------------------------
# Fact Table: Sales
# -----------------------------
fact_rows = []
for tidx in range(1, 1001):
    cust_id = random.choice(customer_df["CustomerID"])
    prod_id = random.choice(product_df["ProductID"])
    time_id = random.choice(time_df["TimeID"])
    store_id = random.choice(store_df["StoreID"])
    price = float(product_df.loc[product_df.ProductID==prod_id,"Price"].values[0])
    units = random.randint(1,10)
    discount = round(random.uniform(0,0.20),2)
    revenue = round(price * units * (1 - discount),2)
    fact_rows.append([tidx,cust_id,prod_id,time_id,store_id,revenue,units,discount])

sales_fact_df = pd.DataFrame(fact_rows,
    columns=["TransactionID","CustomerID","ProductID","TimeID","StoreID","Revenue","UnitsSold","Discount"])

# -----------------------------
# Save to CSVs
# -----------------------------
lookups = {
    "age_group": age_group_df,
    "gender": gender_df,
    "county": county_df,
    "town": town_df,
    "category": category_df,
    "brand": brand_df,
    "quarter": quarter_df,
    "month": month_df,
    "manager": manager_df
}

for name, df in lookups.items():
    df.to_csv(f"{name}_lookup.csv", index=False)

customer_df.to_csv("customer_dim.csv", index=False)
product_df.to_csv("product_dim.csv", index=False)
time_df.to_csv("time_dim.csv", index=False)
store_df.to_csv("store_dim.csv", index=False)
sales_fact_df.to_csv("sales_fact.csv", index=False)

print("Snowflake schema CSVs generated successfully!")
