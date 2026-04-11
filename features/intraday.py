from features.base import FeatureEngine
class IntradayFeatures(FeatureEngine):

    def __init__(self,features:list):
        super().__init__(features)



    def transform(self, df):
        df = df.copy()

        #TODO: can also add volatility, rolling std etc

        if("return" in self.features):
            df["return"] = df["rate"].pct_change()
        
        if("SMA_5" in self.features):
            df["SMA_5"] = df["rate"].rolling(5).mean()

        if("SMA_20" in self.features):
            df["SMA_20"] = df["rate"].rolling(20).mean()
        
        if("EMA_10" in self.features):
            df["EMA_10"] = df["rate"].ewm(span=10,adjust=False).mean()

        return df
        