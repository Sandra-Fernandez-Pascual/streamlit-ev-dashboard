import streamlit as st
from utils import load_data


# Load Data
sales_df, sales_share_df, charging_points_df = load_data()

st.title("EV Dashboard")
st.caption("Global electric vehicle sales and charging infrastructure")

# Sales Data (just for dev)
st.dataframe(sales_df)

# Metrics (TBD)
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F", border=True)
col2.metric("Wind", "9 mph", "-8%", border=True)
col3.metric("Humidity", "86%", "4%", border=True)

st.divider()

# World Sales Chart
st.subheader("World Sales Chart")
world_df = sales_df[sales_df["country"] == "World"]
st.bar_chart(world_df, x="year", y="value", color="powertrain")