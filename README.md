# Anomaly Engine (stock anomaly detection)

This project detects unusual stock price behaviour using a custom Isolation Forest–style model and plots anomaly scores over time. It targets NEPSE-style CSV data and supports both **interday** and **intraday** modes.

## Repository layout

```
Anomaly Engine/
├── main.py                 # Scripted run (train/score/plot)
├── AnomalyDetector.ipynb   # Notebook workflow
├── pyproject.toml            # Package metadata + src layout (pip install -e .)
├── requirements.txt        # Pinned deps for local venvs
├── config/                 # Configuration
├── data/
│   ├── interday/           # One CSV per symbol, e.g. NABIL.csv
│   └── intraday/           # Date folders with per-symbol CSVs
└── src/                    # All importable code (on PYTHONPATH via main/notebook or editable install)
    ├── loaders/
    ├── aggregators/
    ├── features/
    ├── filters/
    ├── models/             # e.g. isolation_forest.py
    ├── engines/
    ├── pipeline/
    ├── analysis/
    └── utils/
```

## Prerequisites

- Python **3.10+** (3.11+ recommended)
- `pip`

## Quickstart

From this directory (`Anomaly Engine/`):

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Option A — run the script**

```bash
python main.py
```

`main.py` adds `src/` to `sys.path` so imports like `pipeline`, `engines`, and `analysis` resolve without an install.

**Option B — editable install (optional)**

```bash
pip install -e .
```

Then you can import `loaders`, `pipeline`, etc. from any working directory (e.g. other notebooks or tools).

**Option C — Jupyter**

Open `AnomalyDetector.ipynb` in VS Code or JupyterLab. The first cell prepends `src/` to `sys.path` when the notebook’s working directory is the repo root (`Anomaly Engine/`).

## Configuring a run

- **Script:** edit variables at the top of `main.py` (`stock_name`, `mode`, date ranges, `features`, `timeframe`, model hyperparameters).
- **Notebook:** edit the parameters cell (`stock_name`, dates, `features`, `n_estimators`, `contamination`, etc.).

Interday loads `data/interday/<SYMBOL>.csv`. Intraday expects files under `data/intraday/<YYYY-MM-DD>/<SYMBOL>.csv` (see `src/loaders/` for details).

## Expected data (high level)

Columns used by the pipeline include timestamp/`transaction_time`, OHLC, and `quantity` where applicable. The pipeline filters and aggregates before feature engineering (SMA/EMA, returns, etc.). Normalize or align raw exports with what `loaders` and `aggregators` expect.

## Outputs

- Console summary of top anomalous periods (when using `main.py`).
- Matplotlib plots from `analysis/matplotlib_visualizer.py` (train and test periods).

## Troubleshooting

**Imports fail in the notebook**

- Set the notebook cwd to `Anomaly Engine/` (the folder that contains `src/`), or run `pip install -e .` and restart the kernel.

**“No such file or directory” for CSVs**

- Interday: ensure `data/interday/<SYMBOL>.csv` exists and matches `stock_name`.
- Intraday: ensure date folders and files exist under `data/intraday/`.

**Jupyter uses the wrong Python**

- Start Jupyter after activating the same venv where you ran `pip install -r requirements.txt`.

## License

This project was developed for educational purposes; data comes from external sources.
