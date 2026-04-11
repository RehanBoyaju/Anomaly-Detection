import pandas as pd

class Filter:
    def filter(self,df,mode:str,columns = None):

        df = df.copy()
        if columns is None:
            columns = ["transaction_time", "rate", "quantity"]


        if mode == "interday":
            df = df.rename(columns={"price":"rate"})
        
        elif mode == "intraday":
            pass
        else:
            raise ValueError(f"Unidentified mode: {mode}")

        df = df[columns]
        df["transaction_time"]=pd.to_datetime(df["transaction_time"])
        

        return df;