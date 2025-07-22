"""ros-rankings
==============
Run the full pipeline with one command::

    python export_json.py

This will update ``outputs/ros_rankings.json`` with the latest projections.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import polars as pl

from src.ingest.fetch_nflfastR import fetch_nflfastr
from src.ingest.fetch_sleeper import fetch_sleeper_players
from src.features.build_features import build_features
from src.modelling.train_weekly import train_weekly_models
from src.modelling.simulate_ros import simulate_ros
from src.evaluation.evaluate_vs_fp import evaluate


def main() -> None:
    seasons = range(2004, 2024)
    fetch_nflfastr(seasons)
    fetch_sleeper_players()
    build_features()
    models = train_weekly_models()
    schedule = pd.DataFrame()  # TODO: real schedule
    ros_df = simulate_ros(models, schedule)
    ros_df = ros_df.with_columns([
        pl.lit(0).alias("pts_ytd"),
        pl.col("ros_proj").alias("on_pace"),
        (pl.col("ros_proj") - pl.col("proj_std")).alias("proj_ci_low"),
        (pl.col("ros_proj") + pl.col("proj_std")).alias("proj_ci_high"),
    ])
    out_path = Path("outputs/ros_rankings.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ros_df.to_pandas().to_json(orient="records"))
    evaluate(ros_df, pd.DataFrame())


if __name__ == "__main__":
    main()
