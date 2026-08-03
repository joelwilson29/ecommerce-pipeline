import random
from datetime import datetime, timedelta
import pandas as pd

from utils.logger import logger

ORDER_STATUSES = [
    "Pending",
    "Shipped",
    "Delivered",
    "Cancelled"
]

ORDER_STATUS_WEIGHTS = [10, 15, 70, 5]

OUTPUT_PATH = "data/bronze/orders.csv"

def generate_order(order_id, customer_id, order_status, order_date):
    """
    Generate a random order record.

    Args:
        order_id (str): The unique identifier for the order.
        customer_id (str): The unique identifier for the customer.
        order_status (str): The status of the order.
        order_date (datetime): The date the order was placed.

    Returns:
        dict: A dictionary containing the generated order data.
    """
    shipping_date = None
    delivery_date = None

    if order_status in ["Shipped", "Delivered"]:
        shipping_date = order_date + timedelta(days=random.randint(1, 5))
        if order_status == "Delivered":
            delivery_date = shipping_date + timedelta(days=random.randint(1, 7))   
    
    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "order_status": order_status,
        "order_date": order_date,
        "shipping_date": shipping_date,
        "delivery_date": delivery_date
    }

    return order

def main():
    logger.info(f"Generating order data...")

    orders = []

    today = datetime.now()

    customers = pd.read_csv("data/bronze/customers.csv")

    customers["registration_date"] = pd.to_datetime(customers["registration_date"])

    for index, customer in customers.iterrows():
        num_of_orders = random.randint(0, 5)
        for _ in range(num_of_orders):
            registration_date = customer["registration_date"]
            diff = today - registration_date
            order_date = registration_date + timedelta(days=random.randint(0, diff.days))
            order_id = f"O{len(orders) + 1:06d}"
            order_status = random.choices(
                ORDER_STATUSES,
                weights=ORDER_STATUS_WEIGHTS,
                k=1
            )[0]
            customer_id = customer["customer_id"]
            order = generate_order(order_id, customer_id, order_status, order_date)
            orders.append(order)

    df = pd.DataFrame(orders)
    df.to_csv(OUTPUT_PATH, index=False)

    logger.info(
        f"Successfully generated {len(df)} orders and saved to {OUTPUT_PATH}"
    )

if __name__ == "__main__":
    main()