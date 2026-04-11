from features.base import base
class InterdayFeatures(base):
    def transform(self,df):
        # Compute return
        df['return'] = df['rate'].pct_change()
        df['rate'] = df['rate'].replace(0, np.nan)

        # Simple Moving Average (SMA)
        df['SMA_5'] = df['rate'].rolling(window=5).mean()  # 5-day moving average
        df['SMA_20'] = df['rate'].rolling(window=20).mean() # 20-day moving average

        # Exponential Moving Average (EMA) identifies trends but reacts faster to recent changes 
        # span is just how fast the memory fades. adjust = false means it the past values are used, and the new value updates the previous EMA recursively.. unlike when adjust = true, for every data point the calculation is done from start

        df['EMA_10'] = df['rate'].ewm(span=10, adjust=False).mean() 

        return df;