import yfinance as yf
import os

ticker = "FOX"

# create the directory if it doesn't exist
if not os.path.exists(f"data/{ticker}"):
    os.makedirs(f"data/{ticker}")

# create Ticker object
shares = yf.Ticker(ticker)

# save share count to CSV
share_count = shares.get_shares_full(start="2022-01-01", end=None)
# share_count["Ticker"] = ticker
share_count.to_csv(f"data/{ticker}/{ticker}_shares.csv")

# save earnings dates to CSV
earnings = shares.earnings_dates
# earnings["Ticker"] = ticker
earnings.to_csv(f"data/{ticker}/{ticker}_earnings.csv")
