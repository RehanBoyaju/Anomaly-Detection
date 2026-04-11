import pandas as pd
from loaders.baseloader import BaseLoader
from utils.paths import INTERDAY
from pathlib import Path
class InterdayLoader(BaseLoader):

    def __init__(self):
        self.base_path = Path(INTERDAY)

    def load(self,stock_name:str,start_date:str,end_date:str):
        df = pd.read_csv(f"data/interday/{stock_name}.csv");
        return df;
