from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent;
print(ROOT);


DATA = ROOT / "data"
INTRADAY = DATA / "intraday"
INTERDAY = DATA / "interday"
OUTPUTS = ROOT / "outputs"
MODELS = ROOT / "models"


