"""Fix data quality (matches experiments notebook logic)."""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data: drop nulls, duplicates, normalize types, filter invalid rows.

    Steps (from experiments notebook):
    1. Drop rows with missing rating_count
    2. Drop duplicates
    3. Convert rating to numeric (coerce errors)
    4. Convert rating_count: strip commas, then float
    5. Convert discounted_price: strip ₹ and commas, float
    6. Convert actual_price: strip ₹ and commas, float
    7. Convert discount_percentage: strip %, float
    8. Drop rows with missing rating
    9. Keep only rows with discount_percentage > 0

    Args:
        df: Raw DataFrame from ingestion.

    Returns:
        Cleaned DataFrame.
    """
    data = df.copy()

    # Drop missing rating_count
    data.dropna(subset=["rating_count"], inplace=True)

    # Drop duplicates
    data.drop_duplicates(inplace=True)

    # Numeric conversions
    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    data["rating_count"] = (
        data["rating_count"].astype(str).str.replace(",", "", regex=False)
    )
    data["rating_count"] = pd.to_numeric(data["rating_count"], errors="coerce")

    data["discounted_price"] = (
        data["discounted_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    data["discounted_price"] = pd.to_numeric(data["discounted_price"], errors="coerce")

    data["actual_price"] = (
        data["actual_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    data["actual_price"] = pd.to_numeric(data["actual_price"], errors="coerce")

    data["discount_percentage"] = (
        data["discount_percentage"].astype(str).str.replace("%", "", regex=False)
    )
    data["discount_percentage"] = pd.to_numeric(
        data["discount_percentage"], errors="coerce"
    )

    # Drop rows with missing rating after conversion
    data.dropna(subset=["rating"], inplace=True)

    # Keep only rows with positive discount
    data = data[data["discount_percentage"] > 0]

    return data.reset_index(drop=True)
