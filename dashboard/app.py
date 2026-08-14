import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_add, lit
import pandas as pd
import sys
from pathlib import Path
import altair as alt

sys.path.append(str(Path(__file__).resolve().parent.parent))

from analytics.sales_metrics import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_average_order_value,
    get_monthly_revenue,
    get_revenue_by_category,
    get_revenue_by_brand,
    get_top_products,
    get_top_customers,
    get_revenue_by_country
)


# --------------------------------------------------
# Streamlit Page
# --------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Sales Dashboard")
st.caption("Sales analytics powered by PySpark and Gold-layer data")


# --------------------------------------------------
# Spark Session
# --------------------------------------------------

spark = (
    SparkSession.builder
        .master("local[*]")
        .appName("E-Commerce Sales Dashboard")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
)


# --------------------------------------------------
# Load Gold Data
# --------------------------------------------------

fact_sales = spark.read.parquet(
    "data/gold/fact_sales"
)

 
# --------------------------------------------------
# Filters
# --------------------------------------------------

st.sidebar.header("Filters")


# -------------------------
# Category
# -------------------------

categories = ["All"] + sorted(
    [
        row["category"]
        for row in fact_sales
            .select("category")
            .distinct()
            .collect()
    ]
)

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)


# -------------------------
# Filter by Category
# -------------------------

category_filtered_df = fact_sales

if selected_category != "All":
    category_filtered_df = category_filtered_df.filter(
        col("category") == selected_category
    )


# -------------------------
# Brand
# -------------------------

brands = ["All"] + sorted(
    [
        row["brand"]
        for row in category_filtered_df
            .select("brand")
            .distinct()
            .collect()
    ]
)

selected_brand = st.sidebar.selectbox(
    "Brand",
    brands
)


# -------------------------
# Filter by Brand
# -------------------------

brand_filtered_df = category_filtered_df

if selected_brand != "All":
    brand_filtered_df = brand_filtered_df.filter(
        col("brand") == selected_brand
    )


# -------------------------
# Country
# -------------------------

countries = ["All"] + sorted(
    [
        row["country"]
        for row in brand_filtered_df
            .select("country")
            .distinct()
            .collect()
    ]
)

selected_country = st.sidebar.selectbox(
    "Country",
    countries
)


# -------------------------
# Date Filter
# -------------------------

st.sidebar.subheader("Order Date")

min_date = fact_sales.selectExpr(
    "MIN(order_date)"
).collect()[0][0].date()

max_date = fact_sales.selectExpr(
    "MAX(order_date)"
).collect()[0][0].date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# -------------------------
# Final Filter
# -------------------------

filtered_fact_sales = brand_filtered_df

if selected_country != "All":
    filtered_fact_sales = filtered_fact_sales.filter(
        col("country") == selected_country
    )

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_fact_sales = filtered_fact_sales.filter(
        (col("order_date") >= lit(start_date))
        & (col("order_date") < date_add(lit(end_date), 1))
    )


# --------------------------------------------------
# Calculate KPIs
# --------------------------------------------------

total_revenue = get_total_revenue(filtered_fact_sales)
total_orders = get_total_orders(filtered_fact_sales)
total_customers = get_total_customers(filtered_fact_sales)
average_order_value = get_average_order_value(filtered_fact_sales)

monthly_revenue = get_monthly_revenue(filtered_fact_sales)
monthly_revenue_pd = monthly_revenue.toPandas()

revenue_by_category = get_revenue_by_category(filtered_fact_sales)  
revenue_by_category_pd = revenue_by_category.toPandas()

revenue_by_brand = get_revenue_by_brand(filtered_fact_sales)
revenue_by_brand_pd = revenue_by_brand.toPandas()

top_products = get_top_products(filtered_fact_sales)
top_products_pd = top_products.toPandas()

top_customers = get_top_customers(filtered_fact_sales)
top_customers_pd = top_customers.toPandas()

revenue_by_country = get_revenue_by_country(filtered_fact_sales)
revenue_by_country_pd = revenue_by_country.toPandas()


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.2f}"
    )

st.subheader("Monthly Revenue Trend")

chart = (
    alt.Chart(monthly_revenue_pd)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "order_month:T",
            title="Month",
            axis=alt.Axis(format="%b %Y")
        ),
        y=alt.Y(
            "revenue:Q",
            title="Revenue"
        ),
        tooltip=[
            alt.Tooltip(
                "order_month:T",
                title="Month",
                format="%b %Y"
            ),
            alt.Tooltip(
                "revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    )
    .properties(
        height=450
    )
)

st.altair_chart(
    chart,
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")

    category_chart = (
        alt.Chart(revenue_by_category_pd)
        .mark_bar()
        .encode(
            x=alt.X(
                "revenue:Q",
                title="Revenue"
            ),
            y=alt.Y(
                "category:N",
                title="Category",
                sort="-x"
            ),
            tooltip=[
                alt.Tooltip("category:N", title="Category"),
                alt.Tooltip(
                    "revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=350)
    )

    st.altair_chart(
        category_chart,
        use_container_width=True
    )


with col2:
    st.subheader("Revenue by Brand")

    brand_chart = (
        alt.Chart(revenue_by_brand_pd)
        .mark_bar()
        .encode(
            x=alt.X(
                "revenue:Q",
                title="Revenue"
            ),
            y=alt.Y(
                "brand:N",
                title="Brand",
                sort="-x"
            ),
            tooltip=[
                alt.Tooltip("brand:N", title="Brand"),
                alt.Tooltip(
                    "revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=350)
    )

    st.altair_chart(
        brand_chart,
        use_container_width=True
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products by Revenue")

    product_chart = (
        alt.Chart(top_products_pd)
        .mark_bar()
        .encode(
            x=alt.X(
                "revenue:Q",
                title="Revenue"
            ),
            y=alt.Y(
                "product_name:N",
                title="Product",
                sort="-x"
            ),
            tooltip=[
                alt.Tooltip(
                    "product_name:N",
                    title="Product"
                ),
                alt.Tooltip(
                    "revenue:Q",
                    title="Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(
        product_chart,
        use_container_width=True
    )


with col2:
    st.subheader("Top 10 Customers by Revenue")

    customer_chart = (
        alt.Chart(top_customers_pd)
        .mark_bar()
        .encode(
            x=alt.X(
                "lifetime_revenue:Q",
                title="Lifetime Revenue"
            ),
            y=alt.Y(
                "customer_name:N",
                title="Customer",
                sort="-x"
            ),
            tooltip=[
                alt.Tooltip(
                    "customer_id:N",
                    title="Customer ID"
                ),
                alt.Tooltip(
                    "customer_name:N",
                    title="Customer"
                ),
                alt.Tooltip(
                    "lifetime_revenue:Q",
                    title="Lifetime Revenue",
                    format=",.0f"
                )
            ]
        )
        .properties(height=400)
    )

    st.altair_chart(
        customer_chart,
        use_container_width=True
    )


st.subheader("Revenue by Country")

chart = (
    alt.Chart(revenue_by_country_pd)
    .mark_bar()
    .encode(
            x=alt.X(
                "country_revenue:Q",
                title="Revenue"
            ),
            y=alt.Y(
                "country:N",
                title="Country",
                sort="-x"
            ),
        tooltip=[
            alt.Tooltip(
                "country:N",
                title="Country"
            ),
            alt.Tooltip(
                "country_revenue:Q",
                title="Revenue",
                format=",.0f"
            )
        ]
    )
    .properties(
        height=450
    )
)

st.altair_chart(
    chart,
    use_container_width=True
)