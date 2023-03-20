import yfinance as yf
import pandas as pd

tickerStrings = ["AAPL", "MSFT"]
for ticker in tickerStrings:
    data = yf.download(ticker, group_by="Ticker")
    data[
        "ticker"
    ] = ticker  # add this column because the dataframe doesn't contain a column with the ticker
    data.to_csv(f"ticker_{ticker}.csv")  # ticker_AAPL.csv for example
