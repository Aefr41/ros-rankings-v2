"""Monte-Carlo simulation of rest-of-season projections."""
from __future__ import annotations

from pathlib import Path
from typing import Dict
import numpy as np
import pandas as pd
import polars as pl

import lightgbm as lgb

POSITIONS = ["QB", "RB", "WR", "TE", "DST"]


def simulate_ros(models: Dict[str, lgb.Booster], schedule: pd.DataFrame, proc_dir: Path = Path("data/processed"), n_sims: int = 1000) -> pl.DataFrame:
    """Run simulations using trained models and upcoming schedule."""
    features = pl.read_parquet(proc_dir / "features.parquet")
    projections = []
    for pos in POSITIONS:
        if pos not in models:
            continue
        pos_df = features.filter(pl.col("position") == pos)
        X = pos_df.drop(["fantasy_points"], axis=1).to_pandas()
        model = models[pos]
        preds = np.stack([model.predict(X) for _ in range(n_sims)], axis=1)
        mean = preds.mean(axis=1)
        std = preds.std(axis=1)
        proj_df = pd.DataFrame({
            "player_id": pos_df["player_id"].to_list(),
            "ros_proj": mean,
            "proj_std": std,
        })
        projections.append(proj_df)
    result = pd.concat(projections, ignore_index=True)
    return pl.from_pandas(result)


if __name__ == "__main__":
    from .train_weekly import train_weekly_models
    models = train_weekly_models()
    schedule = pd.DataFrame()  # TODO: actual schedule
    df = simulate_ros(models, schedule, n_sims=10)
    print(df.head())
