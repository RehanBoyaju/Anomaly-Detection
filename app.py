"""
Flask HTTP API for the anomaly engine.

Run from repo root (``Anomaly Engine/``):

    pip install -r requirements.txt
    python app.py

Or::

    flask --app app run --debug
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.is_dir():
    sys.path.insert(0, str(_SRC))

from flask import Flask, jsonify, request

from services.anomaly_service import run_anomaly_analysis

app = Flask(__name__)


@app.after_request
def _cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/api/analyze", methods=["OPTIONS"])
def analyze_options():
    return "", 204


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/analyze")
def analyze():
    """
    JSON body (see README or sample below). All date fields are ISO-like strings
    accepted by pandas slicing (e.g. ``YYYY-MM-DD``).

    .. code-block:: json

        {
          "stock_name": "NABIL",
          "mode": "Interday",
          "train_start_date": "2025-03-08",
          "train_end_date": "2026-03-08",
          "test_start_date": "2026-03-08",
          "test_end_date": "2026-04-08",
          "timeframe": "1D",
          "features": ["quantity", "return", "SMA_5", "SMA_20", "EMA_10"],
          "n_estimators": 200,
          "contamination": 0.02,
          "top_n": 20,
          "include_test_series": false,
          "test_series_max_rows": 500
        }
    """
    if not request.is_json:
        return jsonify({"error": "Expected Content-Type: application/json"}), 415

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        result = run_anomaly_analysis(payload)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        body: dict = {"error": "Internal server error"}
        if app.debug:
            body["detail"] = traceback.format_exc()
        return jsonify(body), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
