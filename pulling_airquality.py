#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:32:27 2025

@author: mutua
"""

import requests
import pandas as pd
from datetime import datetime

# -------------------
# CONFIG
# -------------------
BASE_URL = "https://api.openaq.org/v3/measurements"
PARAMS = {
    "country": "KE",        # Kenya country code
    "limit": 100,           # number of records per page
    "page": 1,
    "sort": "desc",
    "order_by": "datetime"  # or date
}

# -------------------
# EXTRACT
# -------------------
print("Fetching data from OpenAQ v3 …")
resp = requests.get(BASE_URL, params=PARAMS, timeout=30)
resp.raise_for_status()
data = resp.json()

# -------------------
# TRANSFORM
# -------------------
df = pd.json_normalize(data["results"])

# Add metadata
df["fetched_at"] = datetime.utcnow()
df["country"] = df.get("country", "Unknown")
df["value"] = pd.to_numeric(df.get("value", None), errors="coerce")

print(f"Retrieved {len(df)} rows")

# -------------------
# LOAD — Example: CSV
# -------------------
df.to_csv("openaq_v3_measurements.csv", index=False)
print("Saved to openaq_v3_measurements.csv")

# -------------------
# LOAD — Example: SQLite (optional)
# -------------------
# engine = create_engine("sqlite:///openaq_v3.db")
# df.to_sql("measurements", engine, if_exists="append", index=False)
# print("Loaded into SQLite database openaq_v3.db")
