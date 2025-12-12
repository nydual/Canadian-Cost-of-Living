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

st.markdown('<div class="page-title">⚖️ CPI vs Rent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Compare rent growth with CPI inflation for a chosen province and component.</div>',
    unsafe_allow_html=True,
)

province = st.sidebar.selectbox("Province", sorted(df["Province"].dropna().unique()))
unit_type = st.sidebar.radio("Unit Type", ["1_Bedroom_Rent", "2_Bedroom_Rent"])

# --- Build CPI component choices from the dataframe so names always match
non_cpi_cols = {"Year", "City", "Province", "1_Bedroom_Rent", "2_Bedroom_Rent"}
cpi_candidates = [c for c in df.columns if c not in non_cpi_cols and c != "Month"]

if not cpi_candidates:
    st.error("No CPI columns found in the dataset.")
    st.stop()

cpi_component = st.sidebar.selectbox("CPI Component", sorted(cpi_candidates))

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year), step=1)

df_sel = df[
    (df["Province"] == province)
    & (df["Year"] >= year_range[0])
    & (df["Year"] <= year_range[1])
].copy()

if df_sel.empty:
    st.warning("No data for that selection.")
    st.stop()

# Province-year means
df_year = (
    df_sel.groupby("Year", as_index=False)[[unit_type, cpi_component]]
    .mean()
    .sort_values("Year")
)

# Guard against divide-by-zero in indexing
if df_year[unit_type].iloc[0] in (0, None) or pd.isna(df_year[unit_type].iloc[0]) or \
   df_year[cpi_component].iloc[0] in (0, None) or pd.isna(df_year[cpi_component].iloc[0]):
    st.warning("First year has missing/zero values, so indexed comparison may be unreliable.")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div class="section-title">{unit_type.replace("_"," ")} – {province}</div>',
        unsafe_allow_html=True,
    )
    fig_rent = px.line(
        df_year,
        x="Year",
        y=unit_type,
        markers=True,
        template="plotly_dark",
    )
    fig_rent.update_traces(
        line=dict(width=3, shape="spline", color=COLOR_SEQ[0]),
        marker=dict(size=7),
    )
    fig_rent.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Monthly Rent ($)",
        showlegend=False,
        margin=dict(t=20),
    )
    st.plotly_chart(fig_rent, use_container_width=True)

with col2:
    st.markdown(
        f'<div class="section-title">{cpi_component} – {province}</div>',
        unsafe_allow_html=True,
    )
    fig_cpi = px.line(
        df_year,
        x="Year",
        y=cpi_component,
        markers=True,
        template="plotly_dark",
    )
    fig_cpi.update_traces(
        line=dict(width=3, shape="spline", color=COLOR_SEQ[1]),
        marker=dict(size=7),
    )
    fig_cpi.update_layout(
        xaxis_title="Year",
        yaxis_title="CPI Index",
        showlegend=False,
        margin=dict(t=20),
    )
    st.plotly_chart(fig_cpi, use_container_width=True)

# Indexed comparison
st.markdown(
    '<div class="section-title">Indexed comparison (first year = 100)</div>',
    unsafe_allow_html=True,
)

df_norm = df_year.copy()
df_norm["Rent_index"] = df_norm[unit_type] / df_norm[unit_type].iloc[0] * 100
df_norm["CPI_index"] = df_norm[cpi_component] / df_norm[cpi_component].iloc[0] * 100

df_long = df_norm.melt(
    id_vars="Year",
    value_vars=["Rent_index", "CPI_index"],
    var_name="Series",
    value_name="Index",
)

label_map = {
    "Rent_index": unit_type.replace("_", " "),
    "CPI_index": cpi_component,
}
df_long["Series"] = df_long["Series"].map(label_map)

fig_idx = px.line(
    df_long,
    x="Year",
    y="Index",
    color="Series",
    markers=True,
    template="plotly_dark",
    color_discrete_sequence=[COLOR_SEQ[0], COLOR_SEQ[1]],
)
fig_idx.update_traces(line=dict(width=3, shape="spline"), marker=dict(size=7))
fig_idx.update_layout(
    xaxis_title="Year",
    yaxis_title="Index (first year = 100)",
    legend_title="Series",
    margin=dict(t=20),
)
st.plotly_chart(fig_idx, use_container_width=True)

st.caption(
    "If the rent index rises faster than the CPI index, rents are growing faster than inflation in this period."
)
