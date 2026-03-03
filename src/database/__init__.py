"""Load cleaned data into MySQL."""

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import VARCHAR, TEXT, FLOAT

from ..config import MYSQL_CONFIG, TABLE_NAME


def get_connection_url() -> str:
    """Build MySQL connection URL from config."""
    c = MYSQL_CONFIG
    return (
        f"mysql+pymysql://{c['user']}:{c['password']}@"
        f"{c['host']}:{c['port']}/{c['database']}"
    )


def create_table(engine) -> None:
    """
    Create the amazon_products table if it does not exist.

    Schema matches cleaned CSV columns with appropriate MySQL types.
    """
    sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        product_id VARCHAR(32) NOT NULL,
        product_name VARCHAR(500),
        category VARCHAR(500),
        discounted_price FLOAT,
        actual_price FLOAT,
        discount_percentage FLOAT,
        rating FLOAT,
        rating_count FLOAT,
        about_product TEXT,
        user_id TEXT,
        user_name TEXT,
        review_id TEXT,
        review_title TEXT,
        review_content TEXT,
        img_link TEXT,
        product_link TEXT,
        INDEX idx_product_id (product_id),
        INDEX idx_rating (rating),
        INDEX idx_discount (discount_percentage)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()


def load_to_mysql(
    df: pd.DataFrame,
    table: str | None = None,
    if_exists: str = "replace",
) -> int:
    """
    Load cleaned DataFrame into MySQL.

    Args:
        df: Cleaned DataFrame (from cleaning.clean_data).
        table: Table name. Defaults to config TABLE_NAME.
        if_exists: 'replace' (drop and recreate), 'append', or 'fail'.

    Returns:
        Number of rows written.

    Raises:
        Exception: On connection or write errors.
    """
    table = table or TABLE_NAME
    url = get_connection_url()
    engine = create_engine(url)

    create_table(engine)

    # Map dtypes for MySQL (avoid index column from CSV)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    dtype = {
        "product_id": VARCHAR(32),
        "product_name": VARCHAR(500),
        "category": VARCHAR(500),
        "discounted_price": FLOAT,
        "actual_price": FLOAT,
        "discount_percentage": FLOAT,
        "rating": FLOAT,
        "rating_count": FLOAT,
        "about_product": TEXT,
        "user_id": TEXT,
        "user_name": TEXT,
        "review_id": TEXT,
        "review_title": TEXT,
        "review_content": TEXT,
        "img_link": TEXT,
        "product_link": TEXT,
    }

    n = len(df)
    df.to_sql(
        table,
        engine,
        if_exists=if_exists,
        index=False,
        dtype=dtype,
        method="multi",
        chunksize=500,
    )
    return n
