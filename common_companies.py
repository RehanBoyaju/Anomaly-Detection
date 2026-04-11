from pathlib import Path
import pandas as pd

def get_symbols(folder):
    symbols = set()
    for file in Path(folder).glob("*.csv"):
        symbol = file.stem.strip().upper()
        symbols.add(symbol)

    return symbols

intraday_symbols = get_symbols(Path("../NEPSE_API/data/intraday/2026-04-10"));
interday_symbols = get_symbols(Path("../NepseScraper/data/company-wise"));

common_symbols = intraday_symbols.intersection(interday_symbols)

df = pd.DataFrame(list(common_symbols),columns = ["Symbol"])
df.insert(0,"S.N.",range(1,len(df)+1))

df.to_csv("../data/FinalCompanies.csv",index=False)