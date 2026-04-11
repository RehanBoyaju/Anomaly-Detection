import pandas as pd
from loaders.baseloader import BaseLoader

class InterdayLoader(BaseLoader):
    def load(self,stock_name:str):
        df = pd.read_csv(f"data/interday/{stock_name}.csv");
        return df;
