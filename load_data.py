# Bird Species Observation Analysis Project
# Author: Sarthak Mishra
# Description: Data Cleaning, Analysis, Visualization, and Dashboard
import pandas as pd
import mysql.connector

# Load dataset
df = pd.read_csv(r"C:\Users\DRISHTITA MISHRA\Downloads\bird_project_final\data\cleaned_dataset.csv")

# Select required columns
df = df[[
    "Habitat",
    "Common_Name",
    "Scientific_Name",
    "Year",
    "Month",
    "Temperature",
    "Humidity",
    "Observer",
    "Distance",
    "Flyover_Observed",
    "PIF_Watchlist_Status"
]]

# ✅ Convert NaN to None (VERY IMPORTANT)
df = df.where(pd.notnull(df), None)

# Connect MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sarthak123",
    database="bird_project"
)

cursor = conn.cursor()

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO birds (
            Habitat, Common_Name, Scientific_Name, Year, Month,
            Temperature, Humidity, Observer, Distance,
            Flyover_Observed, PIF_Watchlist_Status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
conn.close()

print("✅ Data inserted successfully!")