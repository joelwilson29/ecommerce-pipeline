from pyspark.sql import SparkSession

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

spark = (
    SparkSession.builder
        .master("local[*]")
        .appName("Test Sales Metrics")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
)

fact_sales = spark.read.parquet(
    "data/gold/fact_sales"
)

total_revenue = get_total_revenue(fact_sales)
total_orders = get_total_orders(fact_sales)
total_customers = get_total_customers(fact_sales)
average_order_value = get_average_order_value(fact_sales)

monthly_revenue = get_monthly_revenue(fact_sales)

monthly_revenue.show(20, truncate=False)

revenue_by_category = get_revenue_by_category(fact_sales)

revenue_by_category.show(truncate=False)

revenue_by_brand = get_revenue_by_brand(fact_sales)

revenue_by_brand.show(truncate=False)

top_products = get_top_products(fact_sales)

top_products.show(truncate=False)

top_customers = get_top_customers(fact_sales)

top_customers.show(truncate=False)

revenue_by_country = get_revenue_by_country(fact_sales)

revenue_by_country.show(truncate=False)

print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Average Order Value:", average_order_value)

spark.stop()