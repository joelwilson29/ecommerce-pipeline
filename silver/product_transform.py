from pyspark.sql.functions import col, trim, initcap, current_timestamp
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Silver Product Transformation")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

df = spark.read.csv("data/bronze/products.csv", header=True, inferSchema=True, multiLine=True)

# Trim Transformation   

trim_columns = [
    "product_id",
    "product_name",
    "category",
    "brand"
]

for column in trim_columns:
    df = df.withColumn(column, trim(col(column)))


# Standardize texts Transformation

title_case_columns = [
    "product_name",
    "category",
    "brand"
]

for column in title_case_columns:
    df = df.withColumn(column, initcap(col(column)))


# Drop duplicates based on product_id

df = df.dropDuplicates(["product_id"])

# Adding Audit columns

df = df.withColumn("etl_load_timestamp", current_timestamp())

# Write the transformed df as parquet to the silver layer

df.write.mode("overwrite").parquet("data/silver/products")