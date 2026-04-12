"""Run the anomaly pipeline and produce JSON-serializable results."""

from __future__ import annotations

import json
import warnings
from typing import Any

import numpy as np
import pandas as pd

from engines.engine import engine
from pipeline.run_pipeline import run_pipeline

warnings.filterwarnings("ignore")

DEFAULT_FEATURES = ["quantity", "return", "SMA_5", "SMA_20", "EMA_10"]


def _df_to_records(df: pd.DataFrame, max_rows: int | None = None) -> list[dict[str, Any]]:
    d = df.copy()
    if d.index.name is None:
        d.index.name = "timestamp"
    d = d.reset_index()
    if max_rows is not None:
        d = d.tail(max_rows)
    return json.loads(d.to_json(orient="records", date_format="iso"))


def run_anomaly_analysis(params: dict[str, Any]) -> dict[str, Any]:
    """
    Execute load → features → Isolation Forest and return structured output.

    Expected keys in ``params`` (all optional except stock_name and date strings):
    stock_name, mode, train_start_date, train_end_date, test_start_date,
    test_end_date, timeframe, features, n_estimators, contamination, top_n,
    include_test_series, test_series_max_rows.
    """
    stock_name = params.get("stock_name")
    if not stock_name:
        raise ValueError("stock_name is required")

    mode = params.get("mode") or "Interday"
    train_start = params.get("train_start_date")
    train_end = params.get("train_end_date")
    test_start = params.get("test_start_date")
    test_end = params.get("test_end_date")
    for label, val in (
        ("train_start_date", train_start),
        ("train_end_date", train_end),
        ("test_start_date", test_start),
        ("test_end_date", test_end),
    ):
        if not val:
            raise ValueError(f"{label} is required")

    timeframe = params.get("timeframe") or ("5min" if mode == "Intraday" else "1D")
    features = params.get("features") or list(DEFAULT_FEATURES)
    if isinstance(features, str):
        features = [x.strip() for x in features.split(",") if x.strip()]

    n_estimators = int(params.get("n_estimators", 200))
    contamination = float(params.get("contamination", 0.02))
    top_n = int(params.get("top_n", 20))
    include_test_series = bool(params.get("include_test_series", False))
    test_series_max_rows = int(params.get("test_series_max_rows", 500))

    X_train, X_test, df_train, df_test = run_pipeline(
        stock_name,
        train_start,
        train_end,
        test_start,
        test_end,
        mode,
        features,
        timeframe,
    )

    if len(X_train) == 0:
        raise ValueError(
            "No training rows after pipeline; check date range and CSV coverage."
        )

    max_depth = int(np.ceil(np.log2(len(X_train))))
    train_scores, test_scores, threshold = engine(
        X_train, X_test, n_estimators, contamination, max_depth
    )

    df_train = df_train.copy()
    df_test = df_test.copy()
    df_train["anomaly_score"] = train_scores
    df_train["anomalous"] = train_scores - threshold < 0
    df_test["anomaly_score"] = test_scores
    df_test["anomalous"] = test_scores - threshold < 0

    top = df_test.sort_values("anomaly_score", ascending=True).head(top_n)
    top_cols = [
        c
        for c in ("close", "quantity", "return", "anomaly_score", "anomalous")
        if c in top.columns
    ]
    top_subset = top[top_cols] if top_cols else top

    out: dict[str, Any] = {
        "stock_name": stock_name,
        "mode": mode,
        "timeframe": timeframe,
        "features": features,
        "threshold": float(threshold),
        "max_depth": max_depth,
        "n_estimators": n_estimators,
        "contamination": contamination,
        "train_rows": int(len(df_train)),
        "test_rows": int(len(df_test)),
        "train_anomalous_count": int(df_train["anomalous"].sum()),
        "test_anomalous_count": int(df_test["anomalous"].sum()),
        "top_anomalies": _df_to_records(top_subset),
    }

    if include_test_series:
        out["test_series"] = _df_to_records(df_test, max_rows=test_series_max_rows)

    return out
