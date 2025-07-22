"""Create model features from raw data."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import polars as pl

from src.utils.scoring import add_fantasy_points


def build_features(raw_dir: Path = Path("data/raw"), proc_dir: Path = Path("data/processed")) -> pl.DataFrame:
    """Process raw data into modeling features."""
    proc_dir.mkdir(parents=True, exist_ok=True)
    weekly = pd.read_parquet(raw_dir / "nflfastr_weekly.parquet")
    weekly = add_fantasy_points(weekly)
    df = pl.from_pandas(weekly)
    df.write_parquet(proc_dir / "features.parquet")
    return df


if __name__ == "__main__":
    df = build_features()
    print(df.head())
