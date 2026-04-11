import pandas as pd
from aggregators.baseaggregator import BaseAggregator
class IntradayAggregator(BaseAggregator):
    def __init__ (self,timeframe:str):
        self.timeframe = timeframe

    def transform(self,df):
        df = df.copy()
        
        df["transaction_time"]=pd.to_datetime(df["transaction_time"])
        df = df.set_index("transaction_time")

        ohlcv = df.resample(self.timeframe).agg(
            open = ("rate","first"),
            high = ("rate","max"),
            low = ("rate","min"),
            close = ("rate","last"),
            volume = ("quantity","sum"),
            amount = ("amount","sum")
        )

        return ohlcv.dropna()
