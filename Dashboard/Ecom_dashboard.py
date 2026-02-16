import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📦 E-Commerce Analytics Dashboard")
st.markdown("---")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

clv_df = load_csv("CLV_table.csv")
monthly_sales_df = load_csv("monthly_sales_with_predictions.csv")
future_sales_df = load_csv("future_3_month_sales_forecast.csv")
rfm_df = load_csv("rfm_customer_segmentation.csv")

# ------------------ KPI SECTION ------------------
st.subheader("🔑 Key Business Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers",
    clv_df["customer_unique_id_x"].nunique()
)

col2.metric(
    "Total Revenue",
    f"₹ {clv_df['TotalRevenue'].sum():,.0f}"
)

col3.metric(
    "Average CLV",
    f"₹ {clv_df['CLV'].mean():,.0f}"
)

st.markdown("---")

# ------------------ CLV TOP 10 ------------------
st.subheader("🏆 Top 10 Customers by CLV")

top10_clv = clv_df.sort_values("CLV", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8,5))
ax.barh(
    top10_clv["customer_unique_id_x"],
    top10_clv["CLV"]
)
ax.set_xlabel("Customer Lifetime Value")
ax.set_ylabel("Customer ID")
ax.invert_yaxis()

st.pyplot(fig)

st.markdown("---")

# ------------------ MONTHLY SALES ------------------
st.subheader("📈 Monthly Sales Trend")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(
    monthly_sales_df["year_month"],
    monthly_sales_df["total_value"],
    label="Actual Sales"
)
ax.plot(
    monthly_sales_df["year_month"],
    monthly_sales_df["predicted_sales"],
    label="Predicted Sales"
)
ax.legend()
plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

# ------------------ FUTURE FORECAST ------------------
st.subheader("🔮 Sales Forecast (Next 3 Months)")

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(
    future_sales_df["Month"],
    future_sales_df["Forecasted_Sales"],
    marker="o"
)
plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

# ------------------ RFM SEGMENTS ------------------
st.subheader("🧠 RFM Customer Segmentation")

segment_counts = rfm_df["Segment"].value_counts()

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(
    segment_counts.index,
    segment_counts.values
)
plt.xticks(rotation=45)
ax.set_ylabel("Number of Customers")

st.pyplot(fig)

st.markdown("---")

# ------------------ RAW DATA (OPTIONAL) ------------------
with st.expander("📂 View Raw Data"):
    st.write("CLV Data", clv_df.head())
    st.write("Monthly Sales Data", monthly_sales_df.head())
    st.write("Forecast Data", future_sales_df)
    st.write("RFM Data", rfm_df.head())