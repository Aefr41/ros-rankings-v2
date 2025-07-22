"""Fetch player data from the Sleeper public API."""
from __future__ import annotations

from pathlib import Path
import requests
import pandas as pd


SLEEPER_URL = "https://api.sleeper.app/v1/players/nfl"


def fetch_sleeper_players(save_dir: Path = Path("data/raw")) -> pd.DataFrame:
    """Download Sleeper player info and cache as JSON."""
    resp = requests.get(SLEEPER_URL, timeout=30)
    resp.raise_for_status()
    players = resp.json()
    df = pd.DataFrame(players.values())
    save_dir.mkdir(parents=True, exist_ok=True)
    (save_dir / "sleeper_players.json").write_text(resp.text)
    return df


if __name__ == "__main__":
    df = fetch_sleeper_players()
    print(df.head())
