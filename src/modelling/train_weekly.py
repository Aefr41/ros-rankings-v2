"""Train weekly LightGBM models per position."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import lightgbm as lgb
import pandas as pd
import polars as pl

POSITIONS = ["QB", "RB", "WR", "TE", "DST"]


def train_weekly_models(proc_dir: Path = Path("data/processed")) -> Dict[str, lgb.Booster]:
    """Train a separate model for each fantasy position."""
    df = pl.read_parquet(proc_dir / "features.parquet").to_pandas()
    models: Dict[str, lgb.Booster] = {}
    for pos in POSITIONS:
        pos_df = df[df["position"] == pos]
        if pos_df.empty:
            continue
        features = [c for c in pos_df.columns if c not in {"fantasy_points", "player_id", "position"}]
        train_data = lgb.Dataset(pos_df[features], label=pos_df["fantasy_points"])
        params = {"objective": "regression", "metric": "rmse"}
        model = lgb.train(params, train_data)
        models[pos] = model
    return models


if __name__ == "__main__":
    models = train_weekly_models()
    print(models.keys())
