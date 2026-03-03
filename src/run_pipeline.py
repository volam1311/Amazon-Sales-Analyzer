#!/usr/bin/env python3
"""
Run the full pipeline: ingestion -> cleaning -> cleaned CSV -> MySQL.

From project root:
  python src/run_pipeline.py
  python -m src.run_pipeline

To skip MySQL and only produce cleaned_data.csv:
  python src/run_pipeline.py --no-db

Requires raw_data.csv in the data/ folder.
For MySQL, set environment variables (see .env.example).
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is on path when run as script (e.g. python src/run_pipeline.py)
_src_dir = Path(__file__).resolve().parent
_project_root = _src_dir.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Amazon DA pipeline")
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Skip loading into MySQL; only ingest, clean, and save CSV",
    )
    parser.add_argument(
        "--no-csv",
        action="store_true",
        help="Skip saving cleaned_data.csv",
    )
    args = parser.parse_args()

    run_pipeline(
        save_cleaned_csv=not args.no_csv,
        load_db=not args.no_db,
    )


if __name__ == "__main__":
    main()
