from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Literal, Optional
from statsmodels.tsa.arima.model import ARIMA


KPILevel = Literal["monthly", "ytd"]


def calculate_kpis(df: pd.DataFrame, actual_col: str, forecast_col: str, date_col: str, level: KPILevel = "monthly") -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["abs_error"] = (df[forecast_col] - df[actual_col]).abs()
    df["bias"] = df[forecast_col] - df[actual_col]
    df["accuracy"] = 1 - df["abs_error"].div(df[actual_col].replace(0, np.nan)).clip(lower=0, upper=1)

    if level == "monthly":
        df["period"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    elif level == "ytd":
        df["period"] = df[date_col].dt.year
    else:
        raise ValueError("Unsupported KPI level")

    grouped = df.groupby("period").agg(
        actual_units=(actual_col, "sum"),
        forecast_units=(forecast_col, "sum"),
        mean_abs_error=("abs_error", "mean"),
        mean_bias=("bias", "mean"),
        accuracy=("accuracy", "mean"),
    )
    grouped = grouped.reset_index()
    return grouped


def performance_with_offset(forecasts: pd.DataFrame, actuals: pd.DataFrame, offset_months: int = 0) -> pd.DataFrame:
    f = forecasts.copy()
    a = actuals.copy()
    f["date"] = pd.to_datetime(f["date"], errors="coerce")
    a["date"] = pd.to_datetime(a["date"], errors="coerce")

    if offset_months != 0:
        f["date"] = f["date"] + pd.DateOffset(months=offset_months)

    merged = (
        f.merge(a, on=["date", "sku", "geolocation", "warehouse"], suffixes=("_f", "_a"))
        .rename(columns={"forecast_units": "forecast_units", "actual_units": "actual_units"})
    )

    return calculate_kpis(merged, actual_col="actual_units", forecast_col="forecast_units", date_col="date", level="monthly")


def statistical_forecast(series: pd.Series, order: tuple[int, int, int] = (1, 1, 1), horizon: int = 12) -> pd.Series:
    series = series.dropna()
    if len(series) < 3:
        return pd.Series(dtype=float)
    model = ARIMA(series, order=order)
    fitted = model.fit()
    forecast = fitted.forecast(steps=horizon)
    forecast.index = pd.date_range(start=series.index.max() + pd.offsets.MonthBegin(), periods=horizon, freq="MS")
    return forecast


def detect_outliers_zscore(data: pd.Series, threshold: float = 3.0) -> pd.DataFrame:
    values = data.astype(float)
    mean = values.mean()
    std = values.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.DataFrame({"value": values, "z": np.zeros_like(values, dtype=float), "is_outlier": False})
    z = (values - mean) / std
    return pd.DataFrame({"value": values, "z": z, "is_outlier": (z.abs() >= threshold)})