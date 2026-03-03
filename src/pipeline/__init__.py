"""Run the full pipeline: ingestion -> cleaning -> CSV export -> MySQL load."""

import logging
from pathlib import Path

from ..config import RAW_DATA_PATH, CLEANED_DATA_PATH, MYSQL_CONFIG
from ..ingestion import load_raw_data
from ..cleaning import clean_data
from ..database import load_to_mysql

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_pipeline(
    raw_path: Path | None = None,
    cleaned_path: Path | None = None,
    save_cleaned_csv: bool = True,
    load_db: bool = True,
) -> int:
    """
    Run the full data pipeline.

    1. Ingest raw data from CSV
    2. Clean data (drop nulls, duplicates, normalize types, filter)
    3. Save cleaned data to CSV (if save_cleaned_csv)
    4. Load cleaned data into MySQL (if load_db)

    Args:
        raw_path: Path to raw CSV. Defaults to config.
        cleaned_path: Path to write cleaned CSV. Defaults to config.
        save_cleaned_csv: Whether to write cleaned_data.csv.
        load_db: Whether to load into MySQL.

    Returns:
        Number of cleaned rows.
    """
    raw_path = raw_path or RAW_DATA_PATH
    cleaned_path = cleaned_path or CLEANED_DATA_PATH

    logger.info("Step 1: Ingesting raw data from %s", raw_path)
    df_raw = load_raw_data(raw_path)
    logger.info("  Loaded %d rows", len(df_raw))

    logger.info("Step 2: Cleaning data")
    df_clean = clean_data(df_raw)
    n = len(df_clean)
    logger.info("  Cleaned to %d rows", n)

    if save_cleaned_csv:
        cleaned_path.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(cleaned_path, index=False)
        logger.info("Step 3: Saved cleaned data to %s", cleaned_path)
    else:
        logger.info("Step 3: Skipped saving cleaned CSV")

    if load_db:
        logger.info("Step 4: Loading into MySQL (%s)", MYSQL_CONFIG.get("database"))
        try:
            load_to_mysql(df_clean)
            logger.info("  Loaded %d rows into MySQL", n)
        except Exception as e:
            logger.error("  MySQL load failed: %s", e)
            raise
    else:
        logger.info("Step 4: Skipped MySQL (load_db=False)")

    return n


def main() -> None:
    """Entry point for running the pipeline from the command line."""
    run_pipeline()
