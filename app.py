import streamlit as st
import pandas as pd
import plotly.express as px


# =====================================
# PAGE CONFIGURATION
# =====================================
st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

st.title("🛍️ Retail Sales Dashboard")

# =====================================
# SIDEBAR
# =====================================
st.sidebar.header("🔍 Dashboard Filters")

# =====================================


# =====================================
# =====================================
# =====================================
# =====================================
# LOAD DATA FROM CSV
# =====================================

df = pd.read_csv("sales_data.csv", sep=";")


# Clean column names
df.columns = (
    df.columns
      .str.strip()          # Remove spaces
      .str.replace('"', '') # Remove quotes
)

# Remove quotes from string values (if any)
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.replace('"', '').str.strip()

# Convert numeric columns
df["quantity"] = pd.to_numeric(df["quantity"])
df["price"] = pd.to_numeric(df["price"])

st.success("✅ Data Loaded Successfully!")

# Uncomment this temporarily if needed for debugging
# st.write(df.columns)

# =====================================
# CREATE REVENUE COLUMN
# =====================================

df["Revenue"] = df["quantity"] * df["price"]

# =====================================
# CREATE MONTH COLUMN
# =====================================
df["Month"] = pd.to_datetime(df["date"]).dt.strftime("%b")

# =====================================
# SIDEBAR FILTERS
# =====================================

city = st.sidebar.multiselect(
    "🏙️ Select City",
    options=sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

category = st.sidebar.multiselect(
    "📦 Select Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

product = st.sidebar.multiselect(
    "🛒 Select Product",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique())
)

# =====================================
# APPLY FILTERS
# =====================================

filtered_df = df[
    (df["city"].isin(city)) &
    (df["category"].isin(category)) &
    (df["product"].isin(product))
]

# =====================================
# KPI CALCULATIONS
# =====================================

total_revenue = filtered_df["Revenue"].sum()
total_orders = len(filtered_df)
total_customers = filtered_df["customer"].nunique()
total_cities = filtered_df["city"].nunique()

# =====================================
# KPI CARDS
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "📦 Total Orders",
        total_orders
    )

with col3:
    st.metric(
        "👥 Total Customers",
        total_customers
    )

with col4:
    st.metric(
        "🏙️ Total Cities",
        total_cities
    )

st.markdown("---")
# =====================================
# REVENUE BY PRODUCT
# =====================================

product_sales = (
    filtered_df.groupby("product")["Revenue"]
        .sum()
        .reset_index()
)

fig_product = px.bar(
    product_sales,
    x="product",
    y="Revenue",
    color="product",
    title="📦 Revenue by Product"
)

st.plotly_chart(fig_product, width="stretch")

# =====================================
# MONTHLY REVENUE TREND
# =====================================

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly_sales = (
    filtered_df.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="📈 Monthly Revenue Trend"
)

st.plotly_chart(fig_month, width="stretch")

# =====================================
# REVENUE BY CITY
# =====================================

city_sales = (
    filtered_df.groupby("city")["Revenue"]
        .sum()
        .reset_index()
)
fig_city = px.bar(
    city_sales,
    x="city",
    y="Revenue",
    color="city",
    title="🏙️ Revenue by City"
)

st.plotly_chart(fig_city, width="stretch")


# =====================================
# CATEGORY WISE REVENUE
# =====================================

category_sales = (
    filtered_df.groupby("category")["Revenue"]
        .sum()
        .reset_index()
)

fig_category = px.pie(
    category_sales,
    names="category",
    values="Revenue",
    title="🥧 Category Wise Revenue"
)

st.plotly_chart(fig_category, width="stretch")

# =====================================
# SALES DATA TABLE
# =====================================

# -------------------------------
# Sales Data
# -------------------------------
st.subheader("📋 Sales Data")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)