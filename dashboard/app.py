import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Canada Cost of Living Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("../data/Final_Cost_of_living_data.csv")

df = load_data()

st.title("🏙️ Canada Cost of Living Dashboard")
st.markdown(
    """
    This dashboard explores rent prices and consumer price index(CPI)
    across Canadian cities and provinces.

    Use the pages in the left sidebar to:
    - Explore rent trends over time
    - Explore CPI components
    - Compare CPI vs rent growth
    - Get quick AI-style narrative insights
    """
)

# Simple KPIs on the home page
latest_year = int(df["Year"].max())
df_latest = df[df["Year"] == latest_year]

avg_1br = df_latest["1_Bedroom_Rent"].mean()
avg_2br = df_latest["2_Bedroom_Rent"].mean()
max_city = df_latest.groupby("City")["1_Bedroom_Rent"].mean().idxmax()
max_rent = df_latest.groupby("City")["1_Bedroom_Rent"].mean().max()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Year", latest_year)
col2.metric("Avg 1BR Rent", f"${avg_1br:,.0f}")
col3.metric("Avg 2BR Rent", f"${avg_2br:,.0f}")
col4.metric("Most Expensive City (1BR)", f"{max_city} (${max_rent:,.0f})")
