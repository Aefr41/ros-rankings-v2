"""Helper functions for working with player/team identifiers."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_player_ids() -> pd.DataFrame:
    """Return mapping of nflverse ids to Sleeper ids.

    If a cached file exists in ``data/raw/player_ids.parquet`` it will be used.
    Otherwise an empty ``DataFrame`` is returned.
    """
    path = Path("data/raw/player_ids.parquet")
    if path.exists():
        return pd.read_parquet(path)
    # TODO: fetch and cache from nflverse once available
    return pd.DataFrame()


if __name__ == "__main__":
    df = load_player_ids()
    print(df.head())
