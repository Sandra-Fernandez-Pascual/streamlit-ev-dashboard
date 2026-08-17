from datetime import date

import plotly.express as px
import streamlit as st
from utils import load_data

# Load Data
sales_df, sales_share_df, charging_points_df = load_data()

st.title("EV Sales")

st.divider()

# EV Sales by Region
st.subheader("EV Sales by Region")

region_options = sorted(sales_df["country"].unique())
default_region_index = region_options.index("World") if "World" in region_options else 0
selected_region = st.selectbox(
    "Region",
    options=region_options,
    index=default_region_index,
    label_visibility="collapsed",
)

region_df = sales_df[sales_df["country"] == selected_region]
st.bar_chart(region_df, x="year", y="value", color="powertrain")

# Top Sales By Country
exclude_groups = ["Other_aggregate", "Projection_region", "European Union", "_World"]
current_year = date.today().year
available_years = sales_df[~sales_df["aggregate_group"].isin(exclude_groups)]["year"].unique()
display_year = max(y for y in available_years if y <= current_year)

st.subheader(f"Top Sales By Country {display_year}")

country_sales = (
    sales_df[~sales_df["aggregate_group"].isin(exclude_groups)]
    .query("year == @display_year")
    .groupby("country", as_index=False)["value"]
    .sum()
    .sort_values("value", ascending=False)
)

top_countries = country_sales.nlargest(10, "value")
pie_fig = px.pie(top_countries, names="country", values="value")
pie_fig.update_layout(
    showlegend=True,
    legend=dict(orientation="v", yanchor="middle", y=0.5, x=1),
    margin=dict(r=120),
)

sales_table = country_sales.rename(columns={"country": "Region", "value": "Cars Sold"})
sales_table["Year"] = display_year

col_pie, col_table = st.columns([2, 1])
with col_pie:
    st.plotly_chart(pie_fig, use_container_width=True)
with col_table:
    st.dataframe(sales_table, use_container_width=True, hide_index=True)

# Sales evolution by country
st.subheader("Top Sales By Country 2023")

country_df = sales_df[~sales_df["aggregate_group"].isin(exclude_groups)]
available_regions = sorted(country_df["country"].unique())
top_regions_2023 = (
    country_df.query("year == 2023")
    .groupby("country", as_index=False)["value"]
    .sum()
    .nlargest(3, "value")["country"]
    .tolist()
)

selected_regions = st.multiselect(
    "Region",
    options=available_regions,
    default=top_regions_2023,
)

powertrain_options = sorted(country_df["powertrain"].unique())
selected_powertrain = st.selectbox("Powertrain", options=powertrain_options)

evolution_df = (
    country_df.query(
        "country in @selected_regions and powertrain == @selected_powertrain"
    )
    .rename(
        columns={
            "country": "Region",
            "year": "Year",
            "powertrain": "Powertrain",
            "value": "Cars sold",
        }
    )
)

line_fig = px.line(
    evolution_df,
    x="Year",
    y="Cars sold",
    color="Region",
    color_discrete_sequence=["blue", "yellow", "green"],
)
st.plotly_chart(line_fig, use_container_width=True)
