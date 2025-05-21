import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# ---- Simulation Setup ---- #
PARTS = ["Brakes", "Engine", "Transmission", "Air Conditioning", "Battery",
         "Tires", "Lights", "Suspension", "Oil Change", "Radiator"]
ISSUES = {
    "Brakes": ["Worn pads", "Brake fluid leak", "ABS failure"],
    "Engine": ["Overheating", "Oil leak", "Misfire", "Timing belt"],
    "Transmission": ["Slipping", "Fluid leak", "Noisy shifting"],
    "Air Conditioning": ["Not cooling", "Refrigerant leak", "Fan issue"],
    "Battery": ["Dead battery", "Corrosion", "Loose connection"],
    "Tires": ["Worn out", "Puncture", "Uneven wear"],
    "Lights": ["Broken headlight", "Signal not working", "Dim lights"],
    "Suspension": ["Shock absorber", "Loose joint", "Squeaking noise"],
    "Oil Change": ["Routine", "Late change", "Oil filter issue"],
    "Radiator": ["Leak", "Clogged", "Fan not working"]
}
PART_COSTS = {
    "Brakes": (300, 800),
    "Engine": (1000, 5000),
    "Transmission": (1500, 6000),
    "Air Conditioning": (500, 2000),
    "Battery": (200, 800),
    "Tires": (400, 1000),
    "Lights": (100, 400),
    "Suspension": (700, 2500),
    "Oil Change": (150, 400),
    "Radiator": (600, 2000)
}

# ---- Functions ---- #
def simulate_maintenance_data(num_buses=100, days_back=365):
    records = []
    for i in range(1, num_buses + 1):
        bus_id = f"BUS-{i:03}"
        visits = random.randint(5, 15)
        for _ in range(visits):
            date = (datetime.now() - timedelta(days=random.randint(1, days_back))).date()
            part = random.choice(PARTS)
            issue = random.choice(ISSUES[part])
            maint_type = random.choice(["Periodic", "Sudden"])
            duration = random.randint(1, 5) if maint_type == "Sudden" else random.randint(1, 2)
            min_cost, max_cost = PART_COSTS[part]
            cost = random.randint(min_cost, max_cost)
            if maint_type == "Sudden":
                cost *= random.uniform(1.1, 1.5)
            records.append({
                "Bus ID": bus_id,
                "Date": date,
                "Part": part,
                "Issue": issue,
                "Maintenance Type": maint_type,
                "Days Out of Service": duration,
                "Maintenance Cost (₪)": round(cost, 2)
            })
    df = pd.DataFrame(records)
    df["Garage Visits"] = df.groupby("Bus ID")["Bus ID"].transform("count")
    return df

# ---- Streamlit UI ---- #
st.set_page_config(page_title="🚌 Bus Maintenance Dashboard", layout="wide")
st.title("🧰 Bus Maintenance Dashboard")

num_buses = st.sidebar.slider("Number of Buses", 10, 150, 100)
top_n = st.sidebar.slider("Top N Costly Buses", 5, num_buses, 10)

data = simulate_maintenance_data(num_buses)
summary = data.groupby("Bus ID").agg({
    "Maintenance Cost (₪)": "sum",
    "Garage Visits": "max",
    "Days Out of Service": "sum"
}).sort_values("Maintenance Cost (₪)", ascending=False)

st.subheader("📊 Maintenance Summary")
st.dataframe(summary.head(top_n))

st.subheader("🧾 Full Maintenance History")
st.dataframe(data)
