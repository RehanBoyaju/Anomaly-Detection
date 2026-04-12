import pandas as pd
from utils.paths import INTRADAY
from pathlib import Path
from loaders.base_loader import BaseLoader
from datetime import datetime
class IntradayLoader(BaseLoader):

    def __init__(self):
        self.base_path = Path(INTRADAY)


    def load(self,stock_name:str,start_date:datetime,end_date:datetime):

        df = self.generate_intraday_data(stock_name,start_date,end_date)
        return df


    def generate_intraday_data(self,stock_name,start_date:datetime,end_date:datetime):

        all_days = []
        
        for date_folder in sorted(self.base_path.iterdir()) :
            if not date_folder.is_dir():
                continue


            date = datetime.strptime(date_folder.name, "%Y-%m-%d")

            

            if(start_date<=date<=end_date):
                file_path = date_folder / f"{stock_name}.csv"

                if file_path.exists():
                    df = pd.read_csv(file_path)
                    df["transaction_time"] = pd.to_datetime(df["transaction_time"])
                    df = df.set_index("transaction_time")
                    df = df.sort_index()
                    
                    
                    all_days.append(df)

        if not all_days:
            #if no data found return an empty dataframe
            return pd.DataFrame()


        #return a concatenated dataframe and ignore the index of the dataframe and generate a brand new set of indices
        return pd.concat(all_days).sort_index()






