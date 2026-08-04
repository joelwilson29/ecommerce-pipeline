from datetime import timedelta

import pandas as pd
from utils.logger import logger
import random

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Wallet"
]

PAYMENT_METHOD_WEIGHTS = [
    45,
    25,
    15,
    10,
    5
]

PAYMENT_STATUS_MAP = {
    "Pending": "Pending",
    "Shipped": "Paid",
    "Delivered": "Paid",
    "Cancelled": "Refunded"
}

OUTPUT_PATH = "data/bronze/payments.csv"

def generate_payment(payment_id, order_id, payment_method, payment_status, payment_date, amount):
    """
    Generate a random payment record.

    Args:
        payment_id (str): The unique identifier for the payment.
        order_id (str): The unique identifier for the order.
        payment_method (str): The method of payment.
        payment_status (str): The status of the payment.
        payment_date (datetime): The date the payment was made.
        amount (float): The amount paid.

    Returns:
        dict: A dictionary containing the generated payment data.
    """
    payment = {
        "payment_id": payment_id,
        "order_id": order_id,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "payment_date": payment_date,
        "amount": amount
    }

    return payment


def main():
    logger.info("Generating payment data...")

    payments = []

    orders = pd.read_csv("data/bronze/orders.csv")
    order_items = pd.read_csv("data/bronze/order_items.csv")

    payment_amount = (
            order_items
            .groupby("order_id", as_index = False)["line_total"]
            .sum()
        )    

    orders["order_date"] = pd.to_datetime(
            orders["order_date"]
        )    

    for _, order in orders.iterrows():
        pay = payment_amount[payment_amount["order_id"] == order["order_id"]]
        amount = pay.iloc[0]["line_total"]
        payment_id = f"PAY{len(payments) + 1:08d}"
        payment_method = random.choices(
            PAYMENT_METHODS,
            weights=PAYMENT_METHOD_WEIGHTS,
            k=1
        )[0]
        payment_status = PAYMENT_STATUS_MAP[
            order["order_status"]
        ]        
        payment_date = (
            order["order_date"] +
            timedelta(days=random.randint(0, 1))
        )  
        order_id = order["order_id"]
        
        payment = generate_payment(payment_id, order_id, payment_method, payment_status, payment_date, amount)
        payments.append(payment)

    df = pd.DataFrame(payments)
    df.to_csv(OUTPUT_PATH, index=False)

    logger.info(
        f"Successfully generated {len(df)} payments and saved to {OUTPUT_PATH}"
    )

if __name__ == "__main__":
    main()