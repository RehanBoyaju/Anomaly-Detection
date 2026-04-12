from pathlib import Path

# Anomaly Engine repo root (directory that contains src/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA = PROJECT_ROOT / "data"
INTRADAY = DATA / "intraday"
INTERDAY = DATA / "interday"
OUTPUTS = PROJECT_ROOT / "outputs"
MODEL_ARTIFACTS = OUTPUTS / "models"
