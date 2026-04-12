import pandas as pd
from aggregators.base_aggregator import BaseAggregator
class IntradayAggregator(BaseAggregator):
    def __init__ (self,timeframe:str,features:list):
        super().__init__(timeframe,features)


    def transform(self,df):
        df = df.copy()
        

        if("quantity" in self.features):
            df = df.resample(self.timeframe).agg(
                open = ("close","first"),
                high = ("close","max"),
                low = ("close","min"),
                close = ("close","last"),
                quantity = ("quantity","sum"),
            )
        else:
            df = df.resample(self.timeframe).agg(
                open = ("close","first"),
                high = ("close","max"),
                low = ("close","min"),
                close = ("close","last"),
            )

        
        
        return df.dropna()
