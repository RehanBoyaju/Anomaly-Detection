from locale import normalize
from pathlib import Path
import pandas as pd
from datetime import date
import sys


# today = str(date.today())
# today = "2026-04-09";
# today = sys.argv[1]

# FinalProject/ when this repo lives under it (src/utils -> +3)
BASE_DIR = Path(__file__).resolve().parents[3]

print(BASE_DIR)


final_symbols = set(pd.read_csv("../../data/FinalCompanies.csv")["Symbol"].str.strip().str.upper());

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
            "contractRate":"rate",
            "contractAmount":"amount"
        },inplace=True)

        df.to_csv(output_dir / f"{symbol}.csv",index=False)


def normalize_interday_columns(input) :

    output_dir = BASE_DIR / "AnomalyEngine" / "data" / "interday"
    output_dir.mkdir(parents=True,exist_ok=True)
    
    for file in Path(input).glob("*.csv") :
        df = pd.read_csv(file)
        symbol = file.stem;

        if symbol not in final_symbols:
            continue

        df.rename(columns={
            "published_date":"transaction_time",
            "traded_quantity":"volume",
            "traded_amount":"amount",
        },inplace=True)

        df.to_csv(output_dir / f"{symbol}.csv",index=False)


def normalize_intraday_test_columns(input,output) :

    for date_folder in Path(input).iterdir() :

        if not date_folder.is_dir(): continue

        date = date_folder.name

        output_dir = Path(output) / date
        output_dir.mkdir(parents=True,exist_ok=True)


        for file in date_folder.glob("*.csv") :

            df = pd.read_csv(file)
            symbol = file.stem

            if symbol not in final_symbols:
                continue

            df.rename(columns={
                "Trade Time":"transaction_time",
                "Quantity":"volume",
                "Rate":"rate",
                "Amount":"amount"
            },inplace=True)

            df.to_csv(output_dir / f"{symbol}.csv",index=False)


# normalize_interday_columns(f"{BASE_DIR}/NepseScraper/data/company-wise")
# normalize_intraday_test_columns(f"{BASE_DIR}/nepse_floorsheet/data/intraday_testing",f"{BASE_DIR}/AnomalyEngine/data/intraday")
# normalize_intraday_columns(f"{BASE_DIR}/NEPSE_API/data/intraday/2026-04-09","../data/intraday/2026-04-09")
# normalize_intraday_columns(f"{BASE_DIR}NEPSE_API/data/intraday/2026-04-10","../data/intraday/2026-04-10")


latest_daily_data = Path(f"{BASE_DIR}/NEPSE_API/data/intraday");

for date_folder in latest_daily_data.iterdir() :
    if not date_folder.is_dir(): continue

    date = date_folder.name
    
    normalize_intraday_columns(date_folder,f"{BASE_DIR}/AnomalyEngine/data/intraday/{date}");
    
    





