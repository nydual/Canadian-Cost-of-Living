import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("../data/Final_Cost_of_living_data.csv")

df = load_data()

st.title("⚖️ CPI vs Rent Comparison")

province = st.sidebar.selectbox("Province", sorted(df["Province"].dropna().unique()))
unit_type = st.sidebar.radio("Unit Type", ["1_Bedroom_Rent", "2_Bedroom_Rent"])

cpi_component = st.sidebar.selectbox(
    "CPI Component",
    [
        "All-items",
        "Shelter",
        "Food",
        "Energy",
        "Gasoline",
        "Transportation",
        "Recreation, education and reading",
    ],
)

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year), step=1)

df_sel = df[
    (df["Province"] == province) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
].copy()

if df_sel.empty:
    st.warning("No data for that selection.")
else:
    df_year = (
        df_sel.groupby("Year", as_index=False)[[unit_type, cpi_component]]
        .mean()
        .sort_values("Year")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{unit_type.replace('_', ' ')} – {province}")
        fig_rent = px.line(
            df_year,
            x="Year",
            y=unit_type,
            markers=True,
            labels={"Year": "Year", unit_type: "Average Monthly Rent ($)"}
        )
        st.plotly_chart(fig_rent, use_container_width=True)

    with col2:
        st.subheader(f"{cpi_component} CPI – {province}")
        fig_cpi = px.line(
            df_year,
            x="Year",
            y=cpi_component,
            markers=True,
            labels={"Year": "Year", cpi_component: "CPI Index"}
        )
        st.plotly_chart(fig_cpi, use_container_width=True)

    # Indexed comparison
    st.subheader("Indexed Comparison (Start Year = 100)")

    df_norm = df_year.copy()
    df_norm["Rent_index"] = df_norm[unit_type] / df_norm[unit_type].iloc[0] * 100
    df_norm["CPI_index"] = df_norm[cpi_component] / df_norm[cpi_component].iloc[0] * 100

    df_long = df_norm.melt(
        id_vars="Year",
        value_vars=["Rent_index", "CPI_index"],
        var_name="Series",
        value_name="Index"
    )

    label_map = {
        "Rent_index": unit_type.replace("_", " "),
        "CPI_index": cpi_component
    }
    df_long["Series"] = df_long["Series"].map(label_map)

    fig_idx = px.line(
        df_long,
        x="Year",
        y="Index",
        color="Series",
        markers=True,
        labels={"Year": "Year", "Index": "Index (Start = 100)", "Series": ""}
    )
    st.plotly_chart(fig_idx, use_container_width=True)

    st.caption(
        "Both series are rebased to 100 in the first year selected. "
        "If the rent line rises faster than the CPI line, rent is growing faster than inflation."
    )
