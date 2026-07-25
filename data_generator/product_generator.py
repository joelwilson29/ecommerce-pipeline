from utils.logger import logger
import pandas as pd
import random
from datetime import datetime, timedelta


OUTPUT_PATH = "data/bronze/products.csv"

CATALOG = {
    "Electronics": {
        "Apple":{
            "iPhone 13": 
                {"min_price": 40000,
                 "max_price": 50000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "MacBook Pro": 
                {"min_price": 100000,
                 "max_price": 200000,
                 "min_stock": 5,
                 "max_stock": 50
            },
            "iPad": 
                {"min_price": 80000,
                 "max_price": 100000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "Samsung":{
            "Galaxy S21": 
                {"min_price": 30000,
                 "max_price": 40000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Galaxy Tab S7": 
                {"min_price": 60000,
                 "max_price": 80000,
                 "min_stock": 5,
                 "max_stock": 50
            },
            "Galaxy Watch": 
                {"min_price": 20000,
                 "max_price": 30000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "Sony":{
            "PlayStation 5": 
                {"min_price": 50000,
                 "max_price": 60000,
                 "min_stock": 5,
                 "max_stock": 50
            },
            "Bravia TV": 
                {"min_price": 70000,
                 "max_price": 90000,
                 "min_stock": 5,
                 "max_stock": 50
            },
            "WH-1000XM4 Headphones": 
                {"min_price": 20000,
                 "max_price": 30000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        }
    },
    "Footwear": {
        "Nike":{
            "Air Max": 
                {"min_price": 8000,
                 "max_price": 12000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Air Force 1": 
                {"min_price": 7000,
                 "max_price": 10000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Air Jordan": 
                {"min_price": 12000,
                 "max_price": 20000,
                 "min_stock": 5,
                 "max_stock": 50
            }
        },
        "Adidas":{
            "Ultraboost": 
                {"min_price": 10000,
                 "max_price": 15000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "NMD": 
                {"min_price": 8000,
                 "max_price": 12000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Stan Smith": 
                {"min_price": 6000,
                 "max_price": 9000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "Puma":{
            "RS-X": 
                {"min_price": 6000,
                 "max_price": 10000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Suede Classic": 
                {"min_price": 5000,
                 "max_price": 8000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Cali": 
                {"min_price": 7000,
                 "max_price": 12000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
    },
    "Books":{
        "Penguin Random House":{
            "The Great Gatsby": 
                {"min_price": 500,
                 "max_price": 1000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Moby Dick": 
                {"min_price": 300,
                 "max_price": 700,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Pride and Prejudice": 
                {"min_price": 400,
                 "max_price": 800,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "HarperCollins":{
            "To Kill a Mockingbird": 
                {"min_price": 600,
                 "max_price": 1200,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "The Catcher in the Rye": 
                {"min_price": 500,
                 "max_price": 1000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "The Hobbit": 
                {"min_price": 700,
                 "max_price": 1500,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "Simon & Schuster":{
            "1984": 
                {"min_price": 400,
                 "max_price": 800,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "The Da Vinci Code": 
                {"min_price": 600,
                 "max_price": 1200,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "The Alchemist": 
                {"min_price": 500,
                 "max_price": 1000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        }
    },
    "Home & Kitchen":{
        "Whirlpool":{
            "Refrigerator": 
                {"min_price": 20000,
                 "max_price": 30000,
                 "min_stock": 5,
                 "max_stock": 50
            },
            "Washing Machine": 
                {"min_price": 15000,
                 "max_price": 25000,
                 "min_stock": 5,
                 "max_stock": 50
            },
            "Microwave Oven": 
                {"min_price": 5000,
                 "max_price": 10000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "Philips":{
            "Air Fryer": 
                {"min_price": 8000,
                 "max_price": 12000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Blender": 
                {"min_price": 3000,
                 "max_price": 6000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Coffee Maker": 
                {"min_price": 4000,
                 "max_price": 8000,
                 "min_stock": 10,
                 "max_stock": 100
            }
        },
        "LG":{
            "Vacuum Cleaner": 
                {"min_price": 10000,
                 "max_price": 15000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Dishwasher": 
                {"min_price": 20000,
                 "max_price": 30000,
                 "min_stock": 10,
                 "max_stock": 100
            },
            "Air Conditioner": 
                {"min_price": 25000,
                 "max_price": 40000,
                 "min_stock": 5,
                 "max_stock": 50
            }
        }
    }  
}


def generate_product(product_id, category, brand, product_name, today):
    """
    Generate a random product record.

    Args:
        product_id (str): The unique identifier for the product.
        category (str): The category of the product.
        brand (str): The brand of the product.
        product_name (str): The name of the product.
        today (datetime): The current date and time.

    Returns:
        dict: A dictionary containing the generated product data.
    """
    details = CATALOG[category][brand][product_name]
    price = random.randint(details["min_price"], details["max_price"])
    stock_quantity = random.randint(details["min_stock"], details["max_stock"])
    random_days = random.randint(0, 365)
    created_date = today - timedelta(days=random_days)
    
    product = {
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "brand": brand,
        "price": price,
        "stock_quantity": stock_quantity,
        "created_date": created_date
    }

    return product

def main():
    logger.info(f"Generating product data...")

    products = []   

    today = datetime.now()

    for category in CATALOG.keys():
        for brand in CATALOG[category].keys():
            for product_name in CATALOG[category][brand].keys():
                product_id = f"P{len(products) + 1:06d}"
                product = generate_product(product_id, category, brand, product_name, today)
                products.append(product)

    df = pd.DataFrame(products)
    df.to_csv(OUTPUT_PATH, index=False)

    logger.info(
        f"Successfully generated {len(df)} products and saved to {OUTPUT_PATH}"
    )

if __name__ == "__main__":
    main()