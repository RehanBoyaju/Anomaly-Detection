from aggregators.base_aggregator import BaseAggregator
class InterdayAggregator(BaseAggregator):
    def __init__ (self,timeframe:str,features:list):
        super().__init__(timeframe,features)

    def transform(self,df):
        df = df.copy()
        
        df = df.set_index("transaction_time")

        if("quantity" in self.features):
            df = df.resample(self.timeframe).agg(
                open = ("open","first"),
                high = ("high","max"),
                low = ("low","min"),
                close = ("close","last"),
                quantity = ("quantity","sum"),
            )
        else:
            df = df.resample(self.timeframe).agg(
                open = ("open","first"),
                high = ("high","max"),
                low = ("low","min"),
                close = ("close","last"),
            )
        
        return df.dropna()
