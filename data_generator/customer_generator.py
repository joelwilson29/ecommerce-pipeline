from utils.logger import logger  
from faker import Faker
from datetime import datetime, timedelta
import random
import pandas as pd

fake = Faker()
NUM_CUSTOMERS = 10000
OUTPUT_PATH = "data/bronze/customers.csv"


def generate_customer(customer_id, today):
    """
    Generate a random customer record.

    Args:
        customer_id (str): The unique identifier for the customer.
        today (datetime): The current date and time.

    Returns:
        dict: A dictionary containing the generated customer data.
    """

    random_days = random.randint(0, 365)
    created_date = today - timedelta(days=random_days)
    registration_date = created_date + timedelta(days=random.randint(0, 30))

    customer = {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "address": fake.address(),
        "city": fake.city(),
        "state": fake.state(),
        "country": fake.country(),
        "pincode": fake.postcode(),
        "created_date": created_date,
        "registration_date": registration_date
    }
    return customer

def main():
    logger.info(f"Generating customer data...")

    customers = []

    # TODO:
    # Generate 10,000 customers
    today = datetime.now()

    for i in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"C{i:06d}"
        customer = generate_customer(customer_id, today)
        customers.append(customer)

    df = pd.DataFrame(customers)
    df.to_csv(OUTPUT_PATH, index=False)

    logger.info(
        f"Successfully generated {len(df)} customers and saved to {OUTPUT_PATH}"
        )


if __name__ == "__main__":
    main()