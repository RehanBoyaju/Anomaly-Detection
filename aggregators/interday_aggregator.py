from aggregators.base_aggregator import BaseAggregator
class InterdayAggregator(BaseAggregator):
    def __init__ (self,timeframe:str,features:list):
        super().__init__(timeframe,features)

    def transform(self,df):
        df = df.copy()
        
        df = df.set_index("transaction_time")

        if("quantity" in self.features):
            ohlcv = df.resample(self.timeframe).agg(
                open = ("rate","first"),
                high = ("rate","max"),
                low = ("rate","min"),
                close = ("rate","last"),
                volume = ("quantity","sum"),
            )
        else:
            ohlcv = df.resample(self.timeframe).agg(
                open = ("rate","first"),
                high = ("rate","max"),
                low = ("rate","min"),
                close = ("rate","last"),
            )
        
        return ohlcv.dropna()
