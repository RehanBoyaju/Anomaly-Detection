from pathlib import Path
import pandas as pd

def get_symbols(folder):
    symbols = set()
    for file in Path(folder).rglob("*.csv"):
        symbol = file.stem.strip().upper()
        symbols.add(symbol)

    return symbols

intraday_symbols = get_symbols(Path("../../NEPSE_API/data/intraday"));
interday_symbols = get_symbols(Path("../../NepseScraper/data/company-wise"));
intraday_test_symbols = get_symbols(Path("../../nepse_floorsheet/data/intraday_testing"));


common_symbols = intraday_symbols & interday_symbols & intraday_test_symbols;

df = pd.DataFrame(list(common_symbols),columns = ["Symbol"])
df.insert(0,"S.N.",range(1,len(df)+1))

output_dir = Path("../data");
output_dir.mkdir(parents=True,exist_ok=True);
df.to_csv(output_dir / "FinalCompanies.csv",index=False)