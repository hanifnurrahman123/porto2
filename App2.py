import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="FMCG Sales EDA", layout="wide")

# =========================
# Load Data
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("D:\DiBimbing Assignment\portofolio\Streamlit Portofolio\FMCG_2022_2024.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.day_name()
    return df

df = load_data()

st.title("📊 FMCG Daily Sales EDA (2022–2024)")
st.markdown("Dataset by Beata Faron")

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("Filter Data")

sku_list = st.sidebar.multiselect("Select SKU", df["sku"].unique())
cat_list = st.sidebar.multiselect("Select Category", df["category"].unique())
year_list = st.sidebar.multiselect("Select Year", df["year"].unique())

filtered_df = df.copy()

if sku_list:
    filtered_df = filtered_df[filtered_df["sku"].isin(sku_list)]
if cat_list:
    filtered_df = filtered_df[filtered_df["category"].isin(cat_list)]
if year_list:
    filtered_df = filtered_df[filtered_df["year"].isin(year_list)]

st.subheader("📌 Filtered Dataset Preview")
st.dataframe(filtered_df.head())

# =========================
# Summary Metrics
# =========================
st.subheader("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(filtered_df):,}")
col2.metric("Total Units Sold", f"{filtered_df['units_sold'].sum():,}")
col3.metric("Avg Price", f"{filtered_df['price_unit'].mean():.2f}")
col4.metric("Promo %", f"{filtered_df['promotion_flag'].mean()*100:.1f}%")

# =========================
# Time Series Plot
# =========================

st.subheader("📅 Daily Sales Trend")

ts = filtered_df.groupby("date")["units_sold"].sum()

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(ts.index, ts.values)
ax.set_title("Daily Total Sales")
ax.set_xlabel("Date")
ax.set_ylabel("Units Sold")
st.pyplot(fig)

# =========================
# Category Breakdown
# =========================
st.subheader("📦 Sales by Category")

cat_sales = filtered_df.groupby("category")["units_sold"].sum().sort_values()

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=cat_sales.values, y=cat_sales.index, ax=ax)
ax.set_title("Total Sales by Category")
st.pyplot(fig)

# Price vs Sales Scatter
# =========================
st.subheader("💸 Price vs Sales Relationship")

fig, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=filtered_df, x="price_unit", y="units_sold", hue="promotion_flag", alpha=0.6)
ax.set_title("Price vs Sold Quantity")
st.pyplot(fig)

# =========================
# Correlation Heatmap
# =========================
st.subheader("🔍 Correlation Heatmap")

num_cols = ["price_unit", "promotion_flag", "delivery_days", "stock_available", "units_sold"]
corr = filtered_df[num_cols].corr()

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("Built by Hanif — Retail Analytics & Pricing Optimization")