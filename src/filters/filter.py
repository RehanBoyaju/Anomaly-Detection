import pandas as pd
import numpy as np


def filter(df, mode: str, columns):

    df = df.copy()

    if mode == "Interday":
        pass
    elif mode == "Intraday":
        df = df.rename(columns={"rate":"close"})
    else:
        raise ValueError(f"Unidentified mode: {mode}")


    df = df[[col for col in columns if col in df.columns]]

    # cols = []
    # for col in columns:
    #     if col in df.columns:
    #         cols.append(col);
    
    # df = df[cols] #i.e df = df["rate","quantity"]

    
    df["close"] = df["close"].replace(0, np.nan)

    # df = df.drop_duplicates();

    return df
