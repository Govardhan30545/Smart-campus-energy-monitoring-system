import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect(r"database\energy.db")

# Read data from database
query = "SELECT * FROM energy_readings"
data = pd.read_sql_query(query, conn)

conn.close()

print("\n========================================")
print("       SMART CAMPUS ENERGY ANALYSIS")
print("========================================")

print("\nTotal records:", len(data))

print("\nColumns:")
print(data.columns.tolist())

print("\nFirst 5 records:")
print(data.head())

# Basic statistics
print("\n========================================")
print("        BASIC STATISTICS")
print("========================================")

print(data.describe())

# Average power consumption
if "Power_W" in data.columns:
    print("\n========================================")
    print("       AVERAGE POWER CONSUMPTION")
    print("========================================")

    average_power = data["Power_W"].mean()
    print(f"Average Power: {average_power:.2f} W")

# Total energy consumption
if "Energy_kWh" in data.columns:
    print("\n========================================")
    print("       TOTAL ENERGY CONSUMPTION")
    print("========================================")

    total_energy = data["Energy_kWh"].sum()
    print(f"Total Energy: {total_energy:.2f} kWh")

# Peak usage
if "Power_W" in data.columns:
    print("\n========================================")
    print("            PEAK USAGE")
    print("========================================")

    peak = data.loc[data["Power_W"].idxmax()]

    print("Building:", peak["Building"])
    print("Power:", peak["Power_W"], "W")
    print("Time:", peak["Timestamp"])

# Building-wise analysis
if "Building" in data.columns and "Power_W" in data.columns:
    print("\n========================================")
    print("       BUILDING-WISE POWER USAGE")
    print("========================================")

    building_usage = data.groupby("Building")["Power_W"].mean()

    print(building_usage)

print("\n========================================")
print("      ANALYSIS COMPLETED SUCCESSFULLY")
print("========================================")