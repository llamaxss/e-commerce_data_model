import pandas as pd
from datetime import datetime, timedelta
import random


def generate_product_data(num_products=100):
    categories = ("Electronics", "Clothing", "Books", "Food")

    products = []
    for i in range(num_products):
        category = random.choice(categories)

        match category:
            case "Electronics":
                base_price = random.uniform(2000, 20000)  # 2000 to 20000 baht
            case "Clothing":
                base_price = random.uniform(199, 1200)  # 199 to 1200 baht
            case "Books":
                base_price = random.uniform(200, 600)  # 200 to 600 baht
            case "Food":
                base_price = random.uniform(50, 500)  # 50 to 500 baht

        product = {
            "product_id": f"PROD_{i+1:05d}",
            "category": category,
            "base_price": round(base_price, 2),
            "stock_quantity": random.randint(0, 1000),
        }
        products.append(product)

    return pd.DataFrame(products)


def generate_customer_data(num_customers=1000):
    domains = ["gmail.com", "hotmail.com", "outlook.com"]

    customers = []
    for i in range(num_customers):
        customer = {
            "customer_id": f"CUST_{i+1:05d}",
            "join_date": (
                datetime.now()
                - timedelta(
                    days=random.randint(0, 365)
                )  # generate join date in the last 1 year
            ).date(),
            "phone_number": "0"
            + "".join([str(random.randint(0, 9)) for _ in range(9)]),
            "email": f"customer_{i+1}@{random.choice(domains)}",
        }
        customers.append(customer)

    return pd.DataFrame(customers)


def generate_order_data(
    customer_df: pd.DataFrame, product_df: pd.DataFrame, num_orders=10000
):
    orders = []
    order_items = []
    package_status = ("Completed", "Shipped", "Processing", "Cancelled")

    customer_ids = customer_df["customer_id"].tolist()
    product_ids = product_df["product_id"].tolist()

    product_prices = product_df[["product_id", "base_price"]].set_index("product_id")

    # Generate orders over the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    for i in range(num_orders):
        order_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )

        order = {
            "order_id": f"ORD_{i+1:05d}",
            "customer_id": random.choice(customer_ids),
            "order_date": order_date,
            "status": random.choice(package_status),
        }
        orders.append(order)

        # Generate 1-5 items per order
        num_items = random.randint(1, 5)
        order_total = 0

        selected_product_ids = random.sample(product_ids, num_items)
        for product_id in selected_product_ids:
            quantity = random.randint(1, 5)
            base_price = product_prices.loc[
                product_id, "base_price"
            ]

            discount = random.choice([0, 0, 0, 0.1, 0.2])  # 60% chance of no discount
            final_price = base_price * (1 - discount)

            order_item = {
                "order_id": order["order_id"],
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": round(final_price, 2),
                "total_price": round(final_price * quantity, 2),
                "discount_applied": discount,
            }
            order_items.append(order_item)
            order_total += order_item["total_price"]

        order["total_amount"] = round(order_total, 2)

    return pd.DataFrame(orders), pd.DataFrame(order_items)


if __name__ == "__main__":
    products_df = generate_product_data()
    customers_df = generate_customer_data()
    orders_df, order_items_df = generate_order_data(customers_df, products_df)

    products_df.to_csv("sample_products.csv", index=False, mode="w")
    customers_df.to_csv("sample_customers.csv", index=False, mode="w")
    orders_df.to_csv("sample_orders.csv", index=False, mode="w")
    order_items_df.to_csv("sample_order_items.csv", index=False, mode="w")
