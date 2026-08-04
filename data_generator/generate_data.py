from data_generator.customer_generator import main as generate_customers
from data_generator.product_generator import main as generate_products
from data_generator.order_generator import main as generate_orders
from data_generator.order_items_generator import main as generate_order_items
from data_generator.payment_generator import main as generate_payments
from utils.logger import logger

def main():

    logger.info("====================================")
    logger.info("Generating Customers...")
    logger.info("====================================")

    generate_customers()

    logger.info("====================================")
    logger.info("Generating Products...")
    logger.info("====================================")

    generate_products()

    logger.info("====================================")
    logger.info("Generating Orders...")
    logger.info("====================================")

    generate_orders()

    logger.info("====================================")
    logger.info("Generating Order Items...")
    logger.info("====================================")

    generate_order_items()

    logger.info("====================================")
    logger.info("Generating Payments...")
    logger.info("====================================")

    generate_payments()

if __name__ == "__main__":
    main()
