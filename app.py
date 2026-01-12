import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Safaricom Financial Analysis", layout="wide")

st.title("📊 Safaricom Financial Analysis Dashboard")

# Load your processed CSVs
summary_df = pd.read_csv("data/processed/safaricom_financial_summary.csv")
income_df = pd.read_csv("data/processed/income_statement_summary.csv")
analysis_df = pd.read_csv("data/processed/safaricom_3year_analysis.csv")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Fiscal Year", analysis_df["Fiscal Year"].unique())

# Revenue vs Net Profit Trend
st.subheader("Revenue vs Net Profit (3-Year Trend)")
fig1 = px.line(
    analysis_df,
    x="Fiscal Year",
    y=["Total Revenue (KShs M)", "Net Profit (KShs M)"],
    markers=True,
    title="Revenue vs Net Profit"
)
st.plotly_chart(fig1, width="stretch")

# Expense Breakdown (Pie Chart)
st.subheader(f"Expense Breakdown for {year}")
year_data = income_df[income_df["Fiscal Year"] == year]

# Melt the dataframe to long format for pie chart
expense_data = year_data.melt(
    id_vars=["Fiscal Year"],
    value_vars=[
        "Direct Costs (KShs M)",
        "Operating Profit (KShs M)",
        "Profit Before Tax (KShs M)",
        "EBITDA (KShs M)"
    ],
    var_name="Expense Category",
    value_name="Amount"
)

fig2 = px.pie(
    expense_data,
    names="Expense Category",
    values="Amount",
    title=f"Expenses in {year}"
)
st.plotly_chart(fig2, width="stretch")

# Financial Ratios
st.subheader("Profitability Ratios")
fig3 = px.bar(
    summary_df,
    x="Fiscal Year",
    y=["Gross_Margin", "Operating_Margin", "Net_Margin"],
    barmode="group",
    title="Margins Over Time"
)
st.plotly_chart(fig3, width="stretch")

