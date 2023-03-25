import yfinance as yf
import pandas as pd


data_folder = "data/"
tickers_file = "tickers.csv"
historical_data_folder = "historical_data/"
shares_folder = "shares/"
earnings_folder = "earnings/"

import yfinance as yf

ticker = "AAPL"
info = yf.Ticker(ticker)._fast_info
for key, value in info.items():
    print(key, value)
# print(f"The latest close price for {ticker} is: {latest_close_price}")
