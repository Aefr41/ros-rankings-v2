"""Fetch basic weather forecasts from the NOAA API."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import requests


def fetch_hourly_forecast(lat: float, lon: float) -> pd.DataFrame:
    """Retrieve hourly forecast for the given location."""
    point_url = f"https://api.weather.gov/points/{lat},{lon}"
    r = requests.get(point_url, timeout=30)
    r.raise_for_status()
    forecast_url = r.json()["properties"]["forecastHourly"]
    f = requests.get(forecast_url, timeout=30)
    f.raise_for_status()
    data = f.json()["properties"]["periods"]
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = fetch_hourly_forecast(39.0997, -94.5786)
    print(df.head())
