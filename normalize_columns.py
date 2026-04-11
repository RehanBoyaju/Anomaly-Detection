from locale import normalize
from pathlib import Path
import pandas as pd
from datetime import date
import sys


# today = str(date.today())
# today = "2026-04-09";
# today = sys.argv[1]

final_symbols = set(pd.read_csv("data/FinalCompanies.csv")["Symbol"].str.strip().str.upper());


def normalize_intraday_columns(input,output) :

    output_dir = Path(output)
    output_dir.mkdir(parents=True,exist_ok=True)
    
    for file in Path(input).glob("*.csv") :
        df = pd.read_csv(file)
        symbol = file.stem;
        # df = df.rename(columns={
        #     "tradeTime":"transaction_time",
        #     "contractQuantity":"quantity",
        #     "contractAmount":"amount"
        # })
        if symbol not in final_symbols:
            continue

        df.rename(columns={
            "tradeTime":"transaction_time",
            "contractQuantity":"quantity",
            "contractRate":"price",
            "contractAmount":"amount"
        },inplace=True)

        df.to_csv(output_dir / f"{symbol}.csv",index=False)


def normalize_interday_columns(input) :

    output_dir = Path(f"data/interday")
    output_dir.mkdir(parents=True,exist_ok=True)
    
    for file in Path(input).glob("*.csv") :
        df = pd.read_csv(file)
        symbol = file.stem;

        if symbol not in final_symbols:
            continue

        df.rename(columns={
            "published_date":"transaction_time",
            "traded_quantity":"quantity",
            "traded_amount":"amount",
        },inplace=True)

        df.to_csv(output_dir / f"{symbol}.csv",index=False)


normalize_intraday_columns("../NEPSE_API/data/intraday/2026-04-09","data/intraday/2026-04-09")
normalize_intraday_columns("../NEPSE_API/data/intraday/2026-04-10","data/intraday/2026-04-10")

normalize_interday_columns(f"../NepseScraper/data/company-wise")
