import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("../data/Final_Cost_of_living_data.csv")

df = load_data()

st.title("🧠 AI-style Insights")

st.subheader("Explain This City")

prov = st.selectbox("Province", sorted(df["Province"].dropna().unique()))
cities = sorted(df.loc[df["Province"] == prov, "City"].dropna().unique())
city = st.selectbox("City", cities)
unit = st.radio("Unit Type", ["1_Bedroom_Rent", "2_Bedroom_Rent"])

city_df = df[(df["Province"] == prov) & (df["City"] == city)].sort_values("Year")

if city_df.empty:
    st.warning("No data for that city.")
else:
    start_year, end_year = int(city_df["Year"].min()), int(city_df["Year"].max())
    start_rent = city_df.loc[city_df["Year"] == start_year, unit].mean()
    end_rent = city_df.loc[city_df["Year"] == end_year, unit].mean()
    rent_change = end_rent - start_rent
    rent_pct = (rent_change / start_rent) * 100 if start_rent > 0 else np.nan

    # simple classification
    if rent_pct > 40:
        label = "very strong rent growth"
    elif rent_pct > 20:
        label = "moderate rent growth"
    elif rent_pct > 5:
        label = "slow but steady rent growth"
    else:
        label = "relatively stable rent levels"

    st.markdown("### Summary")
    st.write(
        f"Between **{start_year}** and **{end_year}**, average "
        f"{unit.replace('_', ' ').lower()} in **{city}, {prov}** increased "
        f"from **${start_rent:,.0f}** to **${end_rent:,.0f}** "
        f"(**{rent_pct:.1f}%**), indicating **{label}**."
    )

    fig = px.line(city_df, x="Year", y=unit, markers=True,
                  labels={"Year": "Year", unit: "Average Monthly Rent ($)"},
                  title=f"{unit.replace('_', ' ')} – {city}")
    st.plotly_chart(fig, use_container_width=True)
