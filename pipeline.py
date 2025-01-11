import pandas as pd
from typing import Optional, Iterable, Union

from database.models import Product, Customer, Order
from database.base import Base, ENGINE, Localsession, Session, Engine


def extract_data() -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        products_df = pd.read_csv("sample_products.csv")
        customers_df = pd.read_csv("sample_customers.csv")
        orders_df = pd.read_csv("sample_orders.csv")
        order_items_df = pd.read_csv("sample_order_items.csv")

        print("Data extraction completed successfully")
        return products_df, customers_df, orders_df, order_items_df

    except Exception as e:
        print(f"Error during data extraction: {e}")
        raise


def order_date_validate(
    customers_df: pd.DataFrame, orders_df: pd.DataFrame
) -> Optional[pd.DataFrame]:
    merged_df = pd.merge(orders_df, customers_df, on="customer_id")
    invalid_orders = merged_df[(merged_df["order_date"] < merged_df["join_date"])].loc[
        :, ["customer_id", "order_id"]
    ]
    return invalid_orders


def transform_data(
    products_df: pd.DataFrame,
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
) -> Union[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        # Convert dates
        customers_df["join_date"] = pd.to_datetime(customers_df["join_date"])
        orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

        # Validate data types
        products_df["base_price"] = products_df["base_price"].astype(float)
        products_df["stock_quantity"] = products_df["stock_quantity"].astype(int)

        # Add data quality checks
        if order_items_df["quantity"].min() <= 0:
            print("Invalid quantities detected in order items")
        date_conflict = order_date_validate(customers_df, orders_df)
        if date_conflict is not None:

            # Remove invalid orders
            orders_df = orders_df[
                ~orders_df["order_id"].isin(date_conflict["order_id"])
            ]
            for data in date_conflict.to_dict(orient="records"):
                print(
                    f"Invalid dates detected in {data['customer_id']}, {data['order_id']}"
                )
            print("Total invalid orders removed:", date_conflict.shape[0])

        print("Data transformation completed successfully")
        return products_df, customers_df, orders_df, order_items_df

    except Exception as e:
        print(f"Error during data transformation: {e}")
        raise


def load_data(
    engine: Engine,
    products_df: pd.DataFrame,
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
) -> None:
    try:
        products_df.to_sql("product", engine, if_exists="append", index=False)
        customers_df.to_sql("customer", engine, if_exists="append", index=False)
        orders_df.to_sql("order", engine, if_exists="append", index=False)
        order_items_df.to_sql("order_item", engine, if_exists="append", index=False)
    except Exception as e:
        print(f"Error during data load: {e}")
        raise


def count_data(session: Session) -> None:
    product_count = session.query(Product).count()
    customer_count = session.query(Customer).count()
    order_count = session.query(Order).count()

    print(
        f"Loaded {product_count} products, {customer_count} customers, {order_count} orders"
    )


def main():
    try:
        # Setup database
        Base.metadata.create_all(ENGINE)

        # Extract
        products_df, customers_df, orders_df, order_items_df = extract_data()

        # Transform
        products_df, customers_df, orders_df, order_items_df = transform_data(
            products_df, customers_df, orders_df, order_items_df
        )

        # Load
        load_data(ENGINE, products_df, customers_df, orders_df, order_items_df)

        with Localsession() as session:
            count_data(session)

        print("ETL process completed successfully")

    except Exception as e:
        print(f"ETL process failed: {e}")
        raise
    finally:
        ENGINE.dispose()


if __name__ == "__main__":
    main()
