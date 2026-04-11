from features.base import FeatureEngine
class InterdayFeatures(FeatureEngine):

    def __init__(self,features:list):
        super().__init__(features)

    def transform(self,df):
        df=df.copy()

        if("return" in self.features):
        # Compute return
            df['return'] = df['rate'].pct_change()
        

        if("SMA_5" in self.features):
            # Simple Moving Average (SMA)
            df['SMA_5'] = df['rate'].rolling(window=5).mean()  # 5-day moving average
        
        if("SMA_20" in self.features):
            df['SMA_20'] = df['rate'].rolling(window=20).mean() # 20-day moving average


        if("EMA_10" in self.features):
            # Exponential Moving Average (EMA) identifies trends but reacts faster to recent changes it calculates the mean of exponential weighted moving values
            # span is just how fast the memory fades. adjust = false means it the past values are used, and the new value updates the previous EMA recursively.. unlike when adjust = true, for every data point the calculation is done from start

            df['EMA_10'] = df['rate'].ewm(span=10, adjust=False).mean() 

        return df;