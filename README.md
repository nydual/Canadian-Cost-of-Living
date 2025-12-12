# 🇨🇦 Canada Cost of Living Analysis
**Rent Prices, Consumer Price Index (CPI), and Inflation Dynamics in Canadian Cities**

## TL;DR  
An end-to-end data science project analyzing rent prices and CPI inflation across Canada, featuring EDA, feature importance modeling, and an interactive Streamlit dashboard.

---

## 📌 Project Overview

This project analyzes cost of living trends in Canada by combining rental market data with Consumer Price Index (CPI) data from Statistics Canada.

**The goal is to understand:**

- How rent prices (1-bedroom and 2-bedroom) have changed across Canadian cities and provinces
- How inflation (CPI) varies by province and component (Shelter, Food, Energy, etc.)
- Whether rent growth is outpacing inflation
- Which CPI components are most associated with rent increases
- How these insights can be communicated through an interactive dashboard

**The project follows a full data science workflow:**

Data Collection → Cleaning → EDA → Feature Engineering → Modeling → Visualization → Dashboard Deployment

---

## 🎯 Key Questions

- How have rental prices evolved over time across Canadian cities?
- Which provinces experience the highest rent growth?
- How does rent growth compare to CPI inflation?
- Are some CPI components more strongly associated with rent increases?
- Can we generate intuitive, non-technical insights for users?

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Modeling | Scikit-learn (Random Forest) |
| Explainability | Permutation Importance, SHAP |
| Dashboard | Streamlit |
| Deployment | Streamlit Community Cloud |
| Data Source | Statistics Canada |

---

## 📂 Project Structure

```
Canada_Cost_of_Living/
│
├── data/
│   ├── raw/
│   │   ├── cpi_raw.csv
│   │   └── rental_raw.csv
│   ├── processed/
│   │   └── Final_Cost_of_Living.csv
│
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb
│   ├── 02_Exploratory_Data_Analysis.ipynb
│   ├── 03_Feature_Importance_Modeling.ipynb
│
├── dashboard/
│   ├── app.py
│   ├── data/
│   │   └── Final_Cost_of_Living.csv
│   └── pages/
│       ├── 1_Rent_Explorer.py
│       ├── 2_CPI_Explorer.py
│       ├── 3_CPI_vs_Rent.py
│       └── 4_AI_Insights.py
│
├── requirements.txt
└── README.md
```

---

## 📊 Data Sources

### Rental Prices

Statistics Canada – Average asking rent by city and unit type

**Unit types analyzed:**
- Apartment – 1 bedroom
- Apartment – 2 bedrooms

### Consumer Price Index (CPI)

Statistics Canada CPI tables

**Components include:**
- All-items
- Shelter
- Food
- Energy
- Gasoline
- Transportation
- Goods & Services
- Recreation, education, and reading

---

## 🧹 Data Cleaning & Preparation

**Notebook:** 

**Key steps:**

- Filtered rental data to relevant unit types
- Standardized geographic labels (cities vs provinces)
- Converted dates into Year and Quarter
- Pivoted rental data to wide format (1BR, 2BR)
- Removed irrelevant CPI aggregates
- Merged CPI and rent data into a single dataset
- Handled missing values carefully (no aggressive imputation)

**Final output:** `data/Final_cost_of_living_data.csv`

---

## 🔍 Exploratory Data Analysis (EDA)

**Notebook:** `02_Exploratory_Data_Analysis.ipynb`

**EDA Highlights:**

- Rent trends over time by city and province
- Comparison of rent levels across cities
- CPI trends by component
- Heatmaps of correlations between rent and CPI components
- Identification of outliers and missing observations

**Key Observations:**

- Rent growth varies significantly across cities
- Shelter CPI does not always move in lockstep with rent
- Some discretionary CPI components correlate strongly with rent due to shared economic trends

---

## 🤖 Modeling & Feature Importance

**Notebook:** `03_Feature_Importance_Modeling.ipynb`

**Approach:**

Random Forest Regression used to predict rent from CPI components

**Feature importance evaluated using:**
- Random Forest impurity-based importance
- Permutation importance


**Key Insight:**

CPI components with smooth, consistent trends (e.g., Recreation, Alcohol & Tobacco) can appear highly predictive — not because they cause rent increases, but because they proxy overall inflation dynamics. This analysis emphasizes correlation vs causation.

---

## 📈 Interactive Dashboard

**Live Dashboard:**

👉 [Add Streamlit link here after deployment]

**Dashboard Pages:**

1. **Rent Explorer**
   - Explore rent trends by city or province
   - Compare 1BR and 2BR units

2. **CPI Explorer**
   - Explore CPI components over time
   - Province-level comparisons

3. **CPI vs Rent**
   - Side-by-side and indexed comparisons
   - Evaluate whether rent outpaces inflation

4. **AI-Style Insights**
   - Automatically generated summaries explaining rent dynamics in plain language

---

## 🚀 Running the Project Locally

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run notebooks:**
```bash
jupyter notebook
```

**Run dashboard:**
```bash
cd dashboard
streamlit run app.py
```

---

## ☁️ Deployment

The dashboard is deployed using Streamlit Community Cloud:

1. Push repository to GitHub
2. Connect GitHub repo on Streamlit Cloud
3. Set main file: `dashboard/app.py`
4. Deploy

---

## 🔮 Future Work

- Add rent affordability index using income data
- Add rent forecasting models
- Expand to additional housing types
- Add interactive geographic maps
- Improve AI-generated explanations using LLMs

---

## ⭐ Acknowledgements

- Statistics Canada for open datasets
- Streamlit for dashboard framework
