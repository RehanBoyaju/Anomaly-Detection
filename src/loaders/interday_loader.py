import pandas as pd
from pathlib import Path

from loaders.base_loader import BaseLoader
from utils.paths import INTERDAY


class InterdayLoader(BaseLoader):

    def __init__(self):
        self.base_path = Path(INTERDAY)

    def load(self, stock_name: str, start_date: str, end_date: str):
        df = pd.read_csv(f"data/interday/{stock_name}.csv")
        return df
