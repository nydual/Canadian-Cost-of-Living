import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

COLOR_SEQ = ["#00c698", "#4c78a8", "#f58518", "#e45756", "#54a24b"]

@st.cache_data
def load_data():
   return pd.read_csv("../data/Final_Cost_of_living_data.csv")

def inject_css():
    st.markdown(
        """
        <style>
        .page-title {
            font-size: 1.7rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .page-subtitle {
            font-size: 0.95rem;
            opacity: 0.85;
            margin-bottom: 0.8rem;
        }
        .section-title {
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 1.0rem;
            margin-bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()

df = load_data()

st.markdown('<div class="page-title">🧠 AI-style Insights</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Pick a city to get a quick narrative summary and see its rent trajectory.</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Explain this city</div>', unsafe_allow_html=True)

prov = st.selectbox("Province", sorted(df["Province"].dropna().unique()))
cities = sorted(df.loc[df["Province"] == prov, "City"].dropna().unique())
city = st.selectbox("City", cities)
unit = st.radio("Unit type", ["1_Bedroom_Rent", "2_Bedroom_Rent"])

city_df = df[(df["Province"] == prov) & (df["City"] == city)].sort_values("Year")

if city_df.empty:
    st.warning("No data for that city.")
else:
    start_year, end_year = int(city_df["Year"].min()), int(city_df["Year"].max())
    start_rent = city_df.loc[city_df["Year"] == start_year, unit].mean()
    end_rent = city_df.loc[city_df["Year"] == end_year, unit].mean()
    rent_change = end_rent - start_rent
    rent_pct = (rent_change / start_rent) * 100 if start_rent > 0 else np.nan

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
        f"{unit.replace('_',' ').lower()} in **{city}, {prov}** increased "
        f"from **${start_rent:,.0f}** to **${end_rent:,.0f}** "
        f"(**{rent_pct:.1f}%**), indicating **{label}**."
    )

    fig = px.line(
    city_df,
    x="Year",
    y=unit,
    markers=True,
    template="plotly_dark",
    )
    fig.update_traces(
    line=dict(width=3, shape="spline", color=COLOR_SEQ[0]),  # teal instead of red
    marker=dict(size=7),
    fill="tozeroy",
    fillcolor="rgba(0,198,152,0.15)",  # soft teal area under the curve
  )
    fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Monthly Rent ($)",
    showlegend=False,
    margin=dict(t=20),
    title=f"{unit.replace('_', ' ')} – {city}",
  )
    st.plotly_chart(fig, use_container_width=True)
 