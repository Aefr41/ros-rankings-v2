"""Download weekly nflfastR data via nfl-data-py."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import pandas as pd
from nfl_data_py import import_weekly_data
from tqdm import tqdm


def fetch_nflfastr(seasons: Iterable[int], save_dir: Path = Path("data/raw")) -> pd.DataFrame:
    """Fetch and cache weekly play-by-play data.

    Parameters
    ----------
    seasons : iterable of int
        Seasons to download.
    save_dir : Path
        Directory to save the combined parquet file.
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    frames: List[pd.DataFrame] = []
    for year in tqdm(list(seasons), desc="nflfastR seasons"):
        frames.append(import_weekly_data([year]))
    df = pd.concat(frames, ignore_index=True)
    out_file = save_dir / "nflfastr_weekly.parquet"
    df.to_parquet(out_file, index=False)
    return df


if __name__ == "__main__":
    df = fetch_nflfastr([2023])
    print(df.head())
