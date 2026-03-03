"""Read raw CSV data."""

import pandas as pd
from pathlib import Path

from ..config import RAW_DATA_PATH


def load_raw_data(path: Path | None = None) -> pd.DataFrame:
    """
    Load raw data from CSV.

    Args:
        path: Optional path to raw CSV. Defaults to config RAW_DATA_PATH.

    Returns:
        DataFrame with raw data.

    Raises:
        FileNotFoundError: If the raw data file does not exist.
    """
    file_path = path or RAW_DATA_PATH
    if not file_path.exists():
        raise FileNotFoundError(f"Raw data file not found: {file_path}")
    return pd.read_csv(file_path)
