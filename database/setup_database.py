import sqlite3
import csv
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "energy_data.csv")
DB_FILE = os.path.join(BASE_DIR, "database", "energy.db")

# Connect to SQLite database
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# Create energy table
cursor.execute("""
CREATE TABLE IF NOT EXISTS energy_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    building TEXT NOT NULL,
    voltage_v REAL,
    current_a REAL,
    power_w REAL,
    energy_kwh REAL
)
""")

# Clear old data if script is run again
cursor.execute("DELETE FROM energy_readings")

# Read CSV and insert data
with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    rows = []

    for row in reader:
        rows.append((
            row["Timestamp"],
            row["Building"],
            float(row["Voltage_V"]),
            float(row["Current_A"]),
            float(row["Power_W"]),
            float(row["Energy_kWh"])
        ))

cursor.executemany("""
INSERT INTO energy_readings
(timestamp, building, voltage_v, current_a, power_w, energy_kwh)
VALUES (?, ?, ?, ?, ?, ?)
""", rows)

connection.commit()

# Check number of records
cursor.execute("SELECT COUNT(*) FROM energy_readings")
count = cursor.fetchone()[0]

connection.close()

print("Database created successfully!")
print(f"Total records inserted: {count}")
print(f"Database saved at: {DB_FILE}")