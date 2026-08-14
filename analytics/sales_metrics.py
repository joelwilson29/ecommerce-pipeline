from pyspark.sql.functions import sum, avg, countDistinct, date_trunc


def get_total_revenue(df):
    return df.agg(
        sum("sales_amount").alias("total_revenue")
    ).collect()[0]["total_revenue"]


def get_total_orders(df):
    return df.select(
        countDistinct("order_id").alias("total_orders")
    ).collect()[0]["total_orders"]


def get_total_customers(df):
    return df.select(
        countDistinct("customer_id").alias("total_customers")
    ).collect()[0]["total_customers"]


def get_average_order_value(df):

    order_totals = (
        df.groupBy("order_id")
          .agg(
              sum("sales_amount").alias("order_total")
          )
    )

    return order_totals.agg(
        avg("order_total").alias("average_order_value")
    ).collect()[0]["average_order_value"]


def get_monthly_revenue(df):
    return (
        df.withColumn(
            "order_month",
            date_trunc("month", "order_date")
        )
        .groupBy("order_month")
        .agg(
            sum("sales_amount").alias("revenue")
        )
        .orderBy("order_month")
    )


def get_revenue_by_category(df):
    return (
        df.groupBy("category")
          .agg(
              sum("sales_amount").alias("revenue")
          )
          .orderBy("revenue", ascending=False)
    )


def get_revenue_by_brand(df):
    return (
        df.groupBy("brand")
          .agg(
              sum("sales_amount").alias("revenue")
          )
          .orderBy("revenue", ascending=False)
    )


def get_top_products(df, n=10):
    return (
        df.groupBy("product_id", "product_name")
          .agg(
              sum("sales_amount").alias("revenue")
          )
          .orderBy("revenue", ascending=False)
          .limit(n)
    )


def get_top_customers(df, n=10):
    return (
        df.groupBy("customer_id", "customer_name")
          .agg(
              sum("sales_amount").alias("lifetime_revenue")
          )
          .orderBy("lifetime_revenue", ascending=False)
          .limit(n)
    )

def get_revenue_by_country(df, n=10):
    return (
        df.groupBy("country")
          .agg(
              sum("sales_amount").alias("country_revenue")
          )
          .orderBy("country_revenue", ascending=False)
          .limit(n)
    )