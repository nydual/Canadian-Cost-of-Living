import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

COLOR_SEQ = ["#00c698", "#4c78a8", "#f58518", "#e45756", "#54a24b"]

@st.cache_data
def load_data():
    # This page is in dashboard/pages/ -> repo root is 2 levels up
    repo_root = Path(__file__).resolve().parents[2]
    csv_path = repo_root / "data" / "Final_Cost_of_living_data.csv"
    return pd.read_csv(csv_path)

def inject_css():
    st.markdown(
        """
        <style>
        .page-title { font-size: 1.7rem; font-weight: 700; margin-bottom: 0.2rem; }
        .page-subtitle { font-size: 0.95rem; opacity: 0.85; margin-bottom: 0.8rem; }
        .section-title { font-size: 1.05rem; font-weight: 600; margin-top: 1.0rem; margin-bottom: 0.35rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_css()
df = load_data()

st.markdown('<div class="page-title">📊 CPI Explorer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Inspect CPI components like Shelter, Food, Energy, and Transportation by province.</div>',
    unsafe_allow_html=True,
)

# --- Sidebar controls
province = st.sidebar.selectbox("Province", sorted(df["Province"].dropna().unique()))

# Build CPI components safely from the CSV columns
non_cpi_cols = {"Year", "City", "Province", "1_Bedroom_Rent", "2_Bedroom_Rent"}
cpi_components = [c for c in df.columns if c not in non_cpi_cols and c != "Month"]
# (If you have other non-CPI columns, add them to non_cpi_cols)

if not cpi_components:
    st.error("No CPI component columns found in the dataset.")
    st.stop()

component = st.sidebar.selectbox("CPI Component", sorted(cpi_components))

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year), step=1)

df_sel = df[
    (df["Province"] == province)
    & (df["Year"] >= year_range[0])
    & (df["Year"] <= year_range[1])
]

if df_sel.empty:
    st.warning("No data for that selection.")
else:
    st.markdown(
        f'<div class="section-title">{component} – {province}</div>',
        unsafe_allow_html=True,
    )

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
        template="plotly_dark",
    )
    fig.update_traces(
        line=dict(width=3, shape="spline", color=COLOR_SEQ[2]),
        marker=dict(size=7),
        fill="tozeroy",
        fillcolor="rgba(245,133,24,0.12)",
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="CPI Index",
        margin=dict(t=20),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
