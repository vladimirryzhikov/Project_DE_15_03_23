import yfinance as yf
import pandas as pd
from datetime import datetime


companies = ["BF.B"]
end_date = datetime.now().strftime("%Y-%m-%d")

tickers = yf.Tickers(companies)
tickers_hist = tickers.history(
    period="max",
    end=end_date,
    interval="1d",
)
tickers_hist.stack(level=1).rename_axis(["Date", "Ticker"]).reset_index(level=1)
print(tickers_hist)
# tickers_hist.to_csv("all_data.csv")
