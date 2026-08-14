from pyspark.sql.functions import col, trim, initcap, current_timestamp
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Silver Order Items Transformation")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

df = spark.read.csv("data/bronze/order_items.csv", header=True, inferSchema=True, multiLine=True)

# Trim Transformation   

trim_columns = [
    "order_item_id",
    "product_id",
    "order_id"
]

for column in trim_columns:
    df = df.withColumn(column, trim(col(column)))

# Drop duplicates based on order_item_id

df = df.dropDuplicates(["order_item_id"])

# Adding Audit columns

df = df.withColumn("etl_load_timestamp", current_timestamp())

# Write the transformed df as parquet to the silver layer

df.write.mode("overwrite").parquet("data/silver/order_items")