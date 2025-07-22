"""Fantasy scoring utilities for full-PPR and 4-pt pass TD leagues."""
from __future__ import annotations

import pandas as pd


PASS_TD_PTS = 4
PPR = 1.0


def add_fantasy_points(df: pd.DataFrame) -> pd.DataFrame:
    """Compute fantasy points according to full-PPR rules.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain standard nflfastR columns.
    """
    df = df.copy()
    df["pass_fp"] = df["pass_td"] * PASS_TD_PTS + df["pass_yds"] / 25 - df["int"] * 2
    df["rush_fp"] = df["rush_td"] * 6 + df["rush_yds"] / 10
    df["rec_fp"] = df["rec_td"] * 6 + df["rec_yds"] / 10 + df["receptions"] * PPR
    df["fantasy_points"] = df["pass_fp"] + df["rush_fp"] + df["rec_fp"]
    return df


if __name__ == "__main__":
    import pandas as pd
    sample = pd.DataFrame({
        "pass_td": [1],
        "pass_yds": [250],
        "int": [0],
        "rush_td": [0],
        "rush_yds": [10],
        "rec_td": [0],
        "rec_yds": [0],
        "receptions": [0],
    })
    out = add_fantasy_points(sample)
    print(out)
