import pandas as pd
import numpy as np

# Number of readings
num_readings = 1000

# Generate timestamps
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    periods=num_readings,
    freq="15min"
)

# Campus buildings
buildings = [
    "Academic Block",
    "Computer Lab",
    "Laboratory",
    "Library",
    "Hostel"
]

# Random building assignment
np.random.seed(42)
building_data = np.random.choice(buildings, num_readings)

# Generate realistic voltage values
voltage = np.random.normal(230, 5, num_readings)

# Generate current values
current = np.random.normal(10, 3, num_readings)

# Calculate power
power = voltage * current

# Calculate energy for 15-minute interval
energy = power * 0.25 / 1000

# Create DataFrame
data = pd.DataFrame({
    "Timestamp": timestamps,
    "Building": building_data,
    "Voltage_V": voltage.round(2),
    "Current_A": current.round(2),
    "Power_W": power.round(2),
    "Energy_kWh": energy.round(4)
})

# Prevent negative values
data["Current_A"] = data["Current_A"].clip(lower=0.5)
data["Power_W"] = data["Power_W"].clip(lower=50)
data["Energy_kWh"] = data["Energy_kWh"].clip(lower=0.01)

# Save dataset
data.to_csv("energy_data.csv", index=False)

print("Energy dataset created successfully!")
print(f"Total readings: {len(data)}")
print("File saved as: energy_data.csv")