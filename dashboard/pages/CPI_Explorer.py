import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
     return pd.read_csv("../data/Final_Cost_of_living_data.csv")

df = load_data()

st.title("📊 CPI Explorer")

province = st.sidebar.selectbox("Province", sorted(df["Province"].dropna().unique()))

component = st.sidebar.selectbox(
    "CPI Component",
    [
        "All-items",
        "Food",
        "Shelter",
        "Energy",
        "Gasoline",
        "Transportation",
        "Goods",
        "Services",
        "Recreation, education and reading",
    ],
)

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year), step=1)

df_sel = df[
    (df["Province"] == province) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

if df_sel.empty:
    st.warning("No data for that selection.")
else:
    trend = (
        df_sel.groupby("Year", as_index=False)[component]
        .mean()
        .sort_values("Year")
    )

    fig = px.line(
        trend,
        x="Year",
        y=component,
        markers=True,
        labels={"Year": "Year", component: "CPI Index"},
        title=f"{component} CPI – {province}"
    )
    st.plotly_chart(fig, use_container_width=True)
