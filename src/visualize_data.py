import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect(r"database\energy.db")
# Read data from database
query = "SELECT * FROM energy_readings"
data = pd.read_sql_query(query, conn)

conn.close()

# Convert timestamp to datetime
data["timestamp"] = pd.to_datetime(data["timestamp"])

print("\n========== ENERGY VISUALIZATION ==========")
print("Total records:", len(data))

# -------------------------------------------------
# 1. Power Usage Over Time
# -------------------------------------------------
plt.figure(figsize=(12, 6))

plt.plot(
    data["timestamp"],
    data["power_w"]
)

plt.xlabel("Time")
plt.ylabel("Power (Watts)")
plt.title("Campus Power Consumption Over Time")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("power_usage_over_time.png")
plt.show()


# -------------------------------------------------
# 2. Average Power Usage by Building
# -------------------------------------------------
building_power = data.groupby("building")["power_w"].mean()

plt.figure(figsize=(10, 6))

building_power.plot(kind="bar")

plt.xlabel("Building")
plt.ylabel("Average Power (Watts)")
plt.title("Average Power Consumption by Building")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("average_power_by_building.png")
plt.show()


# -------------------------------------------------
# 3. Energy Consumption by Building
# -------------------------------------------------
building_energy = data.groupby("building")["energy_kwh"].sum()

plt.figure(figsize=(10, 6))

building_energy.plot(kind="bar")

plt.xlabel("Building")
plt.ylabel("Energy Consumption (kWh)")
plt.title("Total Energy Consumption by Building")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("energy_by_building.png")
plt.show()


print("\n==========================================")
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("Graphs saved in the src folder")
print("==========================================")