from locale import normalize
from pathlib import Path
import pandas as pd
from datetime import date
import sys
import re


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
            "contractQuantity":"volume",
            "contractRate":"price",
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
                "Rate":"price",
                "Amount":"amount"
            },inplace=True)

            df.to_csv(output_dir / f"{symbol}.csv",index=False)


    
def normalize_scraped_floor_data(input="./floorsheet/floor-2026-04-28.csv",output="./../../data/intraday/2026-04-28"):
    
    
    df = pd.read_csv(Path(input), engine="python")

    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    df["transaction_time"] = df["transaction_time"].astype(str)

    # 1. remove commas
    df["transaction_time"] = df["transaction_time"].str.replace(",", "", regex=False)

    # 2. fix ms safely using function
    def fix_ms(ts):
        match = re.match(r"(.*:\d{2}:\d{2}):(\d{1,3}) (AM|PM)", ts)
        if match:
            base = match.group(1)
            ms = match.group(2)

            # normalize to 3 digits safely
            ms = ms.zfill(3)

            return f"{base}.{ms} {match.group(3)}"

        return ts

    df["transaction_time"] = df["transaction_time"].apply(fix_ms)

    # 3. parse datetime
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], errors="coerce")

    # bad_rows = df[df["transaction_time"].isna()]
    # print(bad_rows.head(20))
    
    df= df.rename(columns={
        "quantity":"volume",
        "contractId":"contract_id",
        "buyerMemberId":"buyer_member_id",
        "sellerMemberId":"seller_member_id",
        "rate":"price",
        "stockSymbol":"symbol"
    })
    

    tickers = df["symbol"].unique()

    for ticker in tickers:

        ticker_df = df[df["symbol"] == ticker]
        # Replace any character that is not a letter, number, underscore, or dash with underscore
        safe_ticker = re.sub(r'[^A-Za-z0-9_\-]', '_', ticker)


        ticker_df.to_csv(output_dir / f"{safe_ticker}.csv", index=False)






normalize_interday_columns(f"{BASE_DIR}/NepseScraper/data/company-wise")
normalize_intraday_test_columns(f"{BASE_DIR}/nepse_floorsheet/data/intraday_testing",f"{BASE_DIR}/AnomalyEngine/data/intraday")


latest_daily_data = Path(f"{BASE_DIR}/NEPSE_API/data/intraday");

for date_folder in latest_daily_data.iterdir() :
    if not date_folder.is_dir(): continue

    date = date_folder.name
    
    normalize_intraday_columns(date_folder,f"{BASE_DIR}/AnomalyEngine/data/intraday/{date}");

normalize_scraped_floor_data()



