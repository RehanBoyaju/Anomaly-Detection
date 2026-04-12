import mplfinance as mpf

def plot_ohlcv(stock_name,df,period):
    df_ohlcv = df[['open', 'high', 'low', 'close','quantity']].copy()
    df_ohlcv = df_ohlcv.rename(columns={'quantity':'volume'})
    mpf.plot(
        df_ohlcv,
        type='candle', 
        volume=True, 
        style="yahoo",
        figsize=(50,20),
        title=f"{stock_name} OHLCV {period} data chart",
        volume_panel=1      # Show volume in separate panel
    )
