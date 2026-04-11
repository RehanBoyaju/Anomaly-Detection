class BaseAggregator:
    def __init__ (self,timeframe:str,features:list):
        self.timeframe = timeframe
        self.features = features
    def transform(self,df):
        raise NotImplementedError