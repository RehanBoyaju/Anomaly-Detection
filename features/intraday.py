class IntradayFeatures:
    def __init__(self, window_short=5, window_long=20):
        self.ws = window_short
        self.wl = window_long

    def transform(self, df):
        df["return"] = df["rate"].pct_change()
        df["SMA_short"] = df["rate"].rolling(self.ws).mean()
        df["SMA_long"] = df["rate"].rolling(self.wl).mean()
        return df