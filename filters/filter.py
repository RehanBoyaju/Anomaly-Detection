import pandas as pd
import numpy as np


def filter(self, df, mode: str, columns=None):

    df = df.copy()
    if columns is None:
        columns = ["transaction_time", "rate"]

    if mode == "interday":
        df = df.rename(columns={"close": "rate"})

    elif mode == "intraday":
        pass
    else:
        raise ValueError(f"Unidentified mode: {mode}")

    df = df[columns]
    df["rate"] = df["rate"].replace(0, np.nan)
    df["transaction_time"] = pd.to_datetime(df["transaction_time"])

    return df
