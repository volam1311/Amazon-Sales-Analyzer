"""
Configuration for paths and MySQL connection.
Loads environment variables from a .env file in the project root.
"""

import os
from pathlib import Path
from dotenv import load_dotenv 

# Project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env from project root
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH) 

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw_data.csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_data.csv"

# MySQL connection
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    # default "" avoids None issues if env var missing
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "amazon_da"),
}

# Table name for cleaned product/review data
TABLE_NAME = os.getenv("MYSQL_TABLE", "amazon_products")