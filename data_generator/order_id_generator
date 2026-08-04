import pandas as pd
from utils.logger import logger
import random

OUTPUT_PATH = "data/bronze/order_items.csv"

def generate_order_item(order_item_id, product_id, order_id, quantity, unit_price, line_total):
    """ 
    Generate a unique order item record.
    
    Returns:
        dict: A dictionary containing the generated order item data.
    """

    order_item = {
        "order_item_id": order_item_id,
        "product_id": product_id,
        "order_id": order_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "line_total": line_total
    }

    return order_item

def main():
    logger.info("Generating order items...")

    order_items = []

    products = pd.read_csv("data/bronze/products.csv")
    orders = pd.read_csv("data/bronze/orders.csv")

    for _, row in orders.iterrows():
        num_of_items = random.randint(1,5)
        selected_products = products.sample(n=num_of_items)
        for _, prd in selected_products.iterrows():
            product_id = prd["product_id"]
            order_id = row["order_id"]
            order_item_id = f"OI{len(order_items) + 1:08d}"
            quantity = random.randint(1,3)
            unit_price = prd["price"]
            line_total = quantity * unit_price
    
            order_item = generate_order_item(order_item_id, product_id, order_id, quantity, unit_price, line_total)
            order_items.append(order_item)

    df = pd.DataFrame(order_items)
    df.to_csv(OUTPUT_PATH, index=False)

    logger.info(
        f"Successfully generated {len(df)} order items and saved to {OUTPUT_PATH}"
    )

if __name__ == "__main__":
    main()    