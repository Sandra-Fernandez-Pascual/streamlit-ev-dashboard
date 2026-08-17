import pandas as pd
import streamlit as st

data_path = "data/ev_data.xlsx"

def _clean_parameter_df(df: pd.DataFrame, *, drop_mode: bool = False) -> pd.DataFrame:
    cols_to_drop = ["parameter", "unit"]
    if drop_mode:
        cols_to_drop.append("mode")

    out = (
        df.drop(columns=cols_to_drop)
        .rename(columns={"region_country": "country", "Aggregate group": "aggregate_group"})
    )
    sort_cols = [c for c in ["country", "year", "mode", "powertrain", "category"] if c in out.columns]
    return out.sort_values(sort_cols).reset_index(drop=True)


@st.cache_data
def load_data(path: str = data_path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw = pd.read_excel(path)

    sales_df = _clean_parameter_df(raw[raw["parameter"] == "EV sales"])
    sales_share_df = _clean_parameter_df(raw[raw["parameter"] == "EV sales share"])
    charging_points_df = _clean_parameter_df(
        raw[raw["parameter"] == "EV charging points"], drop_mode=True
    )

    return sales_df, sales_share_df, charging_points_df

