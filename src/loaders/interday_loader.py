import pandas as pd
from pathlib import Path
from datetime import datetime
from loaders.base_loader import BaseLoader
from utils.paths import INTERDAY


class InterdayLoader(BaseLoader):

    def __init__(self):
        self.base_path = Path(INTERDAY)

    def load(self, stock_name: str, start_date, end_date):

        df = pd.read_csv(f"data/interday/{stock_name}.csv")

        df["transaction_time"] = pd.to_datetime(df["transaction_time"]);
        df = df.set_index("transaction_time")
        df = df.sort_index()
        df = df.loc[start_date:end_date]
        return df
