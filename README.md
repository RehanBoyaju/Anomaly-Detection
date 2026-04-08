# Anomaly Engine (Stock Anomaly Detection)

This project detects anomalous stock price behavior using an Isolation Forest–style algorithm and visualizes anomalies over time.

It is designed to run locally with a Jupyter notebook and the CSV files in `data/`.

## What’s in this repo

- `AnomalyDetector.ipynb`: Main notebook (data prep → train/test split → anomaly scoring → plots).
- `SimpleIsolationForest.py`: A small, self-contained Isolation Forest implementation (used by the notebook).
- `data/`: Stock CSV files (example: `data/NABIL.csv`).

## Prerequisites

- Python **3.10+** (3.11 recommended)
- `pip`

## Quickstart (recommended)

From the project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Launch JupyterLab in vscode

Open `AnomalyDetector.ipynb` and run the cells from top to bottom.

## How to choose which stock to run

Inside `AnomalyDetector.ipynb`, edit the parameters cell:

- `stock_name = "NABIL"` → change to the symbol you want (must match a CSV filename in `data/`, without `.csv`)
- `train_start_date`, `train_end_date`
- `test_start_date`, `test_end_date`
- `features`
- `n_estimators`, `contamination`

Example:

- If you set `stock_name = "NMB"`, the notebook will load `data/NMB.csv`.

## Expected data format

The notebook expects each CSV in `data/` to include (at minimum) these columns:

- `published_date` (parsable date/time)
- `close`
- `traded_quantity`

The notebook converts `published_date` to a datetime index and derives technical features like SMA/EMA and returns.

## Outputs

When you run the notebook, you’ll get:

- Time-series plots of price + moving averages
- Highlighted anomaly points
- A histogram of anomaly scores and the model threshold

## Troubleshooting

### Jupyter opens but imports fail

Make sure you launched Jupyter **after** activating the virtual environment:

```bash
source .venv/bin/activate
jupyter lab
```

### “No such file or directory: data/<SYMBOL>.csv”

Confirm the symbol exists in `data/` and matches `stock_name` exactly (case-sensitive).

## License

If you plan to share or publish this project, add a license file (MIT/Apache-2.0/etc.).
