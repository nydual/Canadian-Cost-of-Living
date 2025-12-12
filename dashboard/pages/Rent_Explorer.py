import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

@st.cache_data
def load_data():
    # This page lives in dashboard/pages/ -> repo root is 2 levels up
    repo_root = Path(__file__).resolve().parents[2]
    csv_path = repo_root / "data" / "Final_Cost_of_living_data.csv"
    return pd.read_csv(csv_path)

df = load_data()

st.title("📈 Rent Explorer")

# Sidebar filters
provinces = ["All"] + sorted(df["Province"].dropna().unique().tolist())
selected_province = st.sidebar.selectbox("Province", provinces)

if selected_province == "All":
    city_options = sorted(df["City"].dropna().unique())
else:
    city_options = sorted(df.loc[df["Province"] == selected_province, "City"].dropna().unique())

selected_city = st.sidebar.selectbox("City", ["All"] + city_options)

unit_type = st.sidebar.radio("Unit Type", ["1_Bedroom_Rent", "2_Bedroom_Rent"])

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year), step=1)

# Filter data
df_rent = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

if selected_province != "All":
    df_rent = df_rent[df_rent["Province"] == selected_province]
if selected_city != "All":
    df_rent = df_rent[df_rent["City"] == selected_city]

# --- Line chart: trend ---
if selected_city != "All":
    title_suffix = f"{selected_city}, {selected_province}" if selected_province != "All" else selected_city
    st.subheader(f"Rent Trend – {title_suffix} ({unit_type.replace('_', ' ')})")

    trend = (
        df_rent.groupby("Year", as_index=False)[unit_type]
        .mean()
        .sort_values("Year")
    )

    fig_line = px.line(
        trend,
        x="Year",
        y=unit_type,
        markers=True,
        labels={"Year": "Year", unit_type: "Average Monthly Rent ($)"},
    )
    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.subheader(f"Rent Trend by Province ({unit_type.replace('_', ' ')})")

    trend = (
        df_rent.groupby(["Year", "Province"], as_index=False)[unit_type]
        .mean()
        .sort_values(["Year", "Province"])
    )

    fig_line = px.line(
        trend,
        x="Year",
        y=unit_type,
        color="Province",
        markers=True,
        labels={"Year": "Year", unit_type: "Average Monthly Rent ($)"},
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- Bar chart: latest year comparison ---
st.subheader("Latest Year Rent Comparison")

if not df_rent.empty:
    latest_year = int(df_rent["Year"].max())
    df_latest = df_rent[df_rent["Year"] == latest_year]

    if selected_province != "All":
        group_col = "City"
        title = f"{latest_year} – {unit_type.replace('_', ' ')} by City in {selected_province}"
    else:
        group_col = "Province"
        title = f"{latest_year} – {unit_type.replace('_', ' ')} by Province"

    comparison = (
        df_latest.groupby(group_col, as_index=False)[unit_type]
        .mean()
        .sort_values(unit_type, ascending=False)
    )

    fig_bar = px.bar(
        comparison,
        x=unit_type,
        y=group_col,
        orientation="h",
        labels={unit_type: "Average Monthly Rent ($)", group_col: group_col},
        title=title,
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No data available for this selection.")
