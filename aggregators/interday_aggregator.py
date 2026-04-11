import pandas as pd
from aggregators.base_aggregator import BaseAggregator
class InterdayAggregator(BaseAggregator):
    def __init__ (self,timeframe:str):
        self.timeframe = timeframe

    def transform(self,df):
        df = df.copy()
        
        df = df.set_index("transaction_time")

        ohlcv = df.resample(self.timeframe).agg(

            open = ("close","first"),
            high = ("close","max"),
            low = ("close","min"),
            close = ("close","last"),
            volume = ("quantity","sum"),
            amount = ("amount","sum")
        )

        return ohlcv.dropna()
