import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Canada Cost of Living Dashboard",
    page_icon="🏙️",
    layout="wide",
)

# ---------- CUSTOM CSS ----------
def inject_css():
    st.markdown(
        """
        <style>
        /* Global font + smoothing */
        html, body, [class*="css"]  {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        /* Slightly more breathing room at the very top */
        .block-container {
            padding-top: 1.9rem;
            padding-bottom: 1.6rem;
        }

        /* Header/title wrapper */
        .app-header {
            margin-bottom: 0.8rem;
        }

        /* Title styling */
        .app-title {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: 0.03em;
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }

        /* Logo badge: fully rounded with stronger green/blue gradient + glow */
        .app-title span.logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 52px;
            height: 52px;
            border-radius: 999px;
            background: radial-gradient(circle at 20% 10%, #00e49c, #0b1d78);
            box-shadow: 0 0 22px rgba(0, 228, 156, 0.75);
            font-size: 1.4rem;
        }

        .app-subtitle {
            font-size: 0.98rem;
            opacity: 0.85;
            margin-top: 0.3rem;
            max-width: 900px;
        }

        /* Section heading */
        .section-title {
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 1.8rem;
            margin-bottom: 0.4rem;
        }

        /* Nice bullet list */
        .feature-list li {
            margin-bottom: 0.25rem;
        }

        /* Metric cards */
        .metric-card {
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            background: linear-gradient(
                135deg,
                rgba(0, 228, 156, 0.20),
                rgba(11, 29, 120, 0.90)
            );
            border: 1px solid rgba(0, 228, 156, 0.25);
            box-shadow: 0 14px 30px rgba(0,0,0,0.30);
            backdrop-filter: blur(6px);

            /* subtle animation on hover */
            transition: transform 0.18s ease-out, box-shadow 0.18s ease-out;
        }

        .metric-card:hover {
            transform: translateY(-3px) scale(1.015);
            box-shadow: 0 20px 45px rgba(0,0,0,0.45);
        }

        .metric-label {
            font-size: 0.80rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.80;
            margin-bottom: 0.15rem;
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 700;
        }
        .metric-sub {
            font-size: 0.80rem;
            opacity: 0.86;
            margin-top: 0.18rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("../data/Final_Cost_of_living_data.csv")

df = load_data()

# ---------- LANDING PAGE LAYOUT ----------

st.markdown(
    """
    <div class="app-header">
      <div class="app-title">
          <span class="logo">🏙️</span>
          <span>Canada Cost of Living Dashboard</span>
      </div>
      <div class="app-subtitle">
          Explore how rent prices and consumer price index (CPI) are evolving across Canadian cities and provinces.
          Use the pages in the sidebar to dig into trends, compare regions, and generate quick narrative insights.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# 2-column: description + feature list
c_left, c_right = st.columns([1.4, 1])

with c_left:
    st.markdown(
        """
        <div class="section-title">What you can do here</div>
        <ul class="feature-list">
            <li>Track <b>rent trends</b> for 1-bedroom and 2-bedroom units over time.</li>
            <li>Explore <b>CPI components</b> like Shelter, Food, Energy, and Transportation.</li>
            <li>Compare how <b>rent growth</b> stacks up against <b>inflation</b> in each province.</li>
            <li>Get quick, AI-style summaries of rent dynamics for any city.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

with c_right:
    st.markdown(
        """
        <div class="section-title">Tip</div>
        <p style="font-size:0.92rem; opacity:0.9;">
        Use the navigation in the left sidebar to switch between:
        <b>Rent Explorer</b>, <b>CPI Explorer</b>, <b>CPI vs Rent</b>, and <b>AI Insights</b>.
        </p>
        """,
        unsafe_allow_html=True,
    )

# --- spacer to push cards a bit lower ---
st.markdown("<div style='height: 1.4rem;'></div>", unsafe_allow_html=True)

# ---------- METRICS (LATEST YEAR) ----------
latest_year = int(df["Year"].max())
df_latest = df[df["Year"] == latest_year]

avg_1br = df_latest["1_Bedroom_Rent"].mean()
avg_2br = df_latest["2_Bedroom_Rent"].mean()
max_city = df_latest.groupby("City")["1_Bedroom_Rent"].mean().idxmax()
max_rent = df_latest.groupby("City")["1_Bedroom_Rent"].mean().max()

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Latest Year</div>
            <div class="metric-value">{latest_year}</div>
            <div class="metric-sub">Most recent data in this dashboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Avg 1-Bedroom Rent</div>
            <div class="metric-value">${avg_1br:,.0f}</div>
            <div class="metric-sub">Across all cities in {latest_year}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Avg 2-Bedroom Rent</div>
            <div class="metric-value">${avg_2br:,.0f}</div>
            <div class="metric-sub">Across all cities in {latest_year}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Most Expensive City (1BR)</div>
            <div class="metric-value">{max_city}</div>
            <div class="metric-sub">≈ ${max_rent:,.0f} per month in {latest_year}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
