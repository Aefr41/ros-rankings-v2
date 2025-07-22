"""Evaluate model ranks against realized points and FantasyPros accuracy."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import polars as pl

ACCURACY_FILE = Path("evaluation/accuracy_history.csv")


def evaluate(ranks: pl.DataFrame, realized: pd.DataFrame) -> None:
    """Append a row to ``evaluation/accuracy_history.csv`` with basic metrics."""
    ranks_df = ranks.to_pandas()
    merged = ranks_df.merge(realized, on="player_id", how="left", suffixes=("_proj", "_real"))
    merged["error"] = merged["ros_proj"] - merged["fantasy_points_real"]
    rmse = (merged["error"] ** 2).mean() ** 0.5
    row = {
        "week": realized.get("week", pd.NA).iloc[0] if not realized.empty else pd.NA,
        "rmse": rmse,
    }
    ACCURACY_FILE.parent.mkdir(exist_ok=True, parents=True)
    if ACCURACY_FILE.exists():
        hist = pd.read_csv(ACCURACY_FILE)
        hist = pd.concat([hist, pd.DataFrame([row])], ignore_index=True)
    else:
        hist = pd.DataFrame([row])
    hist.to_csv(ACCURACY_FILE, index=False)


if __name__ == "__main__":
    ranks = pl.DataFrame({"player_id": [1], "ros_proj": [100.0]})
    realized = pd.DataFrame({"player_id": [1], "fantasy_points_real": [90.0]})
    evaluate(ranks, realized)
    print(ACCURACY_FILE.read_text())
