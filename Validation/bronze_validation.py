from utils.logger import logger
import pandas as pd

customers = pd.read_csv("data/bronze/customers.csv")
products = pd.read_csv("data/bronze/products.csv")
orders = pd.read_csv("data/bronze/orders.csv")
order_items = pd.read_csv("data/bronze/order_items.csv")
payments = pd.read_csv("data/bronze/payments.csv")


# Validate function for customer dataset
def validate_customers(customers):

    validation_failed = False

    validation_failed |= check_unique(
        customers,
        "customer_id"
    )

    validation_failed |= check_nulls(
        customers,
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "created_date",
            "registration_date"
        ]
    )

    # registration_date >= created_date

    # registration_date <= today

    return validation_failed

# Validate function for product dataset
def validate_products(products):

    validation_failed = False

    validation_failed |= check_unique(
        products,
        "product_id"
    )

    validation_failed |= check_nulls(
        products,
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "price",
            "stock_quantity"
        ]
    )

    validation_failed |= check_positive(
        products,
        "price"
    )

    return validation_failed

# Validate function for order dataset
def validate_orders(orders):

    validation_failed = False

    validation_failed |= check_unique(
        orders,
        "order_id"
    )

    validation_failed |= check_nulls(
        orders,
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_date"
        ]
    )

    # customer_id exists in customers

    # order_date >= registration_date

    # Pending -> shipping_date, delivery_date = NULL

    # Shipped -> shipping_date NOT NULL

    # Delivered -> shipping_date and delivery_date NOT NULL

    # Cancelled -> shipping_date and delivery_date NULL

    return validation_failed

# Validate function for order_item dataset
def validate_order_items(order_items):

    validation_failed = False

    validation_failed |= check_unique(
        order_items,
        "order_item_id"
    )

    validation_failed |= check_nulls(
        order_items,
        [
            "order_item_id",
            "product_id",
            "order_id",
            "quantity",
            "unit_price",
            "line_total"
        ]
    )

    validation_failed |= check_positive(
        order_items,
        "quantity"
    )

    validation_failed |= check_positive(
        order_items,
        "unit_price"
    )

    validation_failed |= check_positive(
        order_items,
        "line_total"
    )

    # order_id exists in orders

    # product_id exists in products

    # line_total == quantity * unit_price

    return validation_failed

# Validate function for payment dataset
def validate_payments(payments):

    validation_failed = False

    validation_failed |= check_unique(
        payments,
        "payment_id"
    )

    validation_failed |= check_nulls(
        payments,
        [
            "payment_id",
            "order_id",
            "payment_method",
            "payment_status",
            "payment_date",
            "amount"
        ]
    )

    validation_failed |= check_positive(
        payments,
        "amount"
    )

    # payment amount == SUM(line_total)

    # payment_status matches order_status

    # payment_date >= order_date

    return validation_failed

#Validation check for duplicates
def check_unique(df, column_name):
    """
    Check if the values in a specified column of a DataFrame are unique.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        column_name (str): The name of the column to check for uniqueness.

    Returns:
        bool: True if the values in the column are duplicates, False otherwise.
    """
    has_duplicates = False

    if df[column_name].duplicated().any():
        has_duplicates = True
        duplicates = df[df[column_name].duplicated()][column_name]

        logger.error(
            f"{column_name} contains duplicate values:\n{duplicates}"
        )

    if not has_duplicates:
        logger.info(f"{column_name} is unique.")

    return has_duplicates

#Validation check for Null values
def check_nulls(df, required_columns):
    """
    Check if there are any null values in the specified columns of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        required_columns (list): A list of column names to check for null values.

    Returns:
        bool: True if there are null values in any of the specified columns, False otherwise.
    """
    has_nulls = False

    for column_name in required_columns:
        if df[column_name].isnull().any():
            has_nulls = True
            null_count = df[column_name].isnull().sum()

            logger.error(
                f"{column_name} contains {null_count} null value(s)."
            )

    if not has_nulls:
        logger.info("No null values found.")

    return has_nulls

#Validation check for Positive values
def check_positive(df, column_name):
    """
    Check that all values in a column are positive (> 0).

    Args:
        df (pd.DataFrame): The DataFrame to check.
        column_name (str): The name of the column to check for positive values.


    Returns:
        bool: True if all values in the column are non-positive, False otherwise.
    """
    has_non_positive = False

    if(df[column_name] <= 0).any():
        has_non_positive = True
        non_positive_values_count = (df[column_name] <= 0).sum()

        logger.error(
            f"{column_name} contains {non_positive_values_count} non-positive value(s)."
        )

    if not has_non_positive:
        logger.info(f"No non-positive values found in {column_name}.")

    return has_non_positive
    

def main():

    logger.info("Starting Bronze validation...")

    validation_failed = False

    validation_failed |= validate_customers(customers)

    validation_failed |= validate_products(products)

    validation_failed |= validate_orders(orders)

    validation_failed |= validate_order_items(order_items)

    validation_failed |= validate_payments(payments)

    if validation_failed:
        logger.error("Bronze validation failed.")
    else:
        logger.info("Bronze validation passed.")

if __name__ == "__main__":
    main()