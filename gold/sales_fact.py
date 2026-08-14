from pyspark.sql.functions import col, concat_ws, current_timestamp
from utils.logger import logger
from pyspark.sql import SparkSession

spark = (SparkSession.builder
             .master("local[*]")
             .appName("Gold Sales Fact Transformation")
             .config("spark.driver.host", "127.0.0.1")
             .config("spark.driver.bindAddress", "127.0.0.1")
             .getOrCreate()
        )

logger.info("Starting Gold Sales Fact Transformation")

order_items_df = spark.read.parquet("data/silver/order_items")
customers_df = spark.read.parquet("data/silver/customers")
orders_df = spark.read.parquet("data/silver/orders")
products_df = spark.read.parquet("data/silver/products")
payments_df = spark.read.parquet("data/silver/payments")


sales_fact_df = (
    order_items_df.alias("oi")
        .join(orders_df.alias("o"), "order_id", "left")
        .join(customers_df.alias("c"), "customer_id", "left")
        .join(products_df.alias("p"), "product_id", "left")
        .join(payments_df.alias("pay"), "order_id", "left")
)


sales_fact_df = sales_fact_df.select(

    # Order
    col("oi.order_item_id"),
    col("oi.order_id"),

    col("o.order_date"),
    col("o.order_status"),

    # Customer
    col("c.customer_id"),
    concat_ws(
        " ",
        col("c.first_name"),
        col("c.last_name")
    ).alias("customer_name"),
    col("c.city"),
    col("c.state"),
    col("c.country"),

    # Product
    col("p.product_id"),
    col("p.product_name"),
    col("p.category"),
    col("p.brand"),

    # Sales
    col("oi.quantity"),
    col("oi.unit_price").alias("selling_price"),
    col("oi.line_total").alias("sales_amount"),

    # Payment
    col("pay.payment_method"),
    col("pay.payment_status")   
)


sales_fact_df = sales_fact_df.withColumn(
    "gold_etl_timestamp",
    current_timestamp()
)


sales_fact_df.write.mode("overwrite").parquet("data/gold/fact_sales")

logger.info("Gold Sales Fact created successfully")
