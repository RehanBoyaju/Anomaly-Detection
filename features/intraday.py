import numpy as np
class IntradayFeatures:


    def transform(self, df):
        df = df.copy()

        #TODO: can also add volatility, rolling std etc
        df["return"] = df["rate"].pct_change()
        df['rate'] = df['rate'].replace(0, np.nan)
        df["SMA_5"] = df["rate"].rolling(5).mean()
        df["SMA_10"] = df["rate"].rolling(10).mean()
        df["EMA_10"] = df["rate"].ewm(span=10,adjust=False).mean()

        return df
        