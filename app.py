import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Smart Campus Energy Monitoring",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
DB_PATH = "database/energy.db"

conn = sqlite3.connect(DB_PATH)

data = pd.read_sql_query(
    "SELECT * FROM energy_readings",
    conn
)

conn.close()

# Convert timestamp
data["timestamp"] = pd.to_datetime(data["timestamp"])

# -----------------------------
# TITLE
# -----------------------------
st.title("⚡ Smart Campus Energy Monitoring System")
st.write("IoT-based Energy Monitoring and Big Data Analytics Dashboard")

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Dashboard Filters")

buildings = ["All"] + sorted(data["building"].unique().tolist())

selected_building = st.sidebar.selectbox(
    "Select Building",
    buildings
)

if selected_building != "All":
    filtered_data = data[data["building"] == selected_building]
else:
    filtered_data = data

# -----------------------------
# KEY METRICS
# -----------------------------
total_records = len(filtered_data)
average_power = filtered_data["power_w"].mean()
maximum_power = filtered_data["power_w"].max()
total_energy = filtered_data["energy_kwh"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    total_records
)

col2.metric(
    "Average Power",
    f"{average_power:.2f} W"
)

col3.metric(
    "Peak Power",
    f"{maximum_power:.2f} W"
)

col4.metric(
    "Total Energy",
    f"{total_energy:.2f} kWh"
)

st.divider()

# -----------------------------
# POWER CONSUMPTION GRAPH
# -----------------------------
st.subheader("📈 Power Consumption Over Time")

fig, ax = plt.subplots()

ax.plot(
    filtered_data["timestamp"],
    filtered_data["power_w"]
)

ax.set_xlabel("Time")
ax.set_ylabel("Power (W)")
ax.set_title("Campus Power Consumption")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# BUILDING COMPARISON
# -----------------------------
st.subheader("🏢 Energy Consumption by Building")

building_energy = (
    filtered_data
    .groupby("building")["energy_kwh"]
    .sum()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots()

building_energy.plot(
    kind="bar",
    ax=ax2
)

ax2.set_xlabel("Building")
ax2.set_ylabel("Energy (kWh)")
ax2.set_title("Energy Consumption by Building")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig2)

# -----------------------------
# VOLTAGE AND CURRENT
# -----------------------------
st.subheader("🔌 Voltage and Current")

col1, col2 = st.columns(2)

with col1:
    fig3, ax3 = plt.subplots()

    ax3.plot(
        filtered_data["timestamp"],
        filtered_data["voltage_v"]
    )

    ax3.set_xlabel("Time")
    ax3.set_ylabel("Voltage (V)")
    ax3.set_title("Voltage Monitoring")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig3)

with col2:
    fig4, ax4 = plt.subplots()

    ax4.plot(
        filtered_data["timestamp"],
        filtered_data["current_a"]
    )

    ax4.set_xlabel("Time")
    ax4.set_ylabel("Current (A)")
    ax4.set_title("Current Monitoring")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig4)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📊 Energy Sensor Data")

st.dataframe(
    filtered_data,
    use_container_width=True
)

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.success(
    "Smart Campus Energy Monitoring Dashboard is running successfully."
)