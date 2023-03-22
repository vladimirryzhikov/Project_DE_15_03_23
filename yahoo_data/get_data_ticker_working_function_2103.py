import yfinance as yf
import os

ticker = "APPL"  # WORKING FUNCTIONS ODF DATA TICKER TESTED ON MSFT NEED TO LOOP OVER ALL TICKETS AND ADD THE CODE TO WORKING SCRIPT

# create the directory if it doesn't exist
if not os.path.exists(f"data/{ticker}"):
    os.makedirs(f"data/{ticker}")


# create Ticker object
msft = yf.Ticker(ticker)

# get historical market data and save to CSV
hist = msft.history(period="1mo")
hist.to_csv(f"data/{ticker}/msft_history.csv")

# save actions to CSV
msft.actions.to_csv(f"data/{ticker}/msft_actions.csv")
msft.dividends.to_csv(f"data/{ticker}msft_dividends.csv")
msft.splits.to_csv(f"data/{ticker}msft_splits.csv")

# save share count to CSV
msft.get_shares_full(start="2022-01-01", end=None).to_csv(
    f"data/{ticker}/msft_shares.csv"
)


# save holders to CSV
msft.major_holders.to_csv(f"data/{ticker}/msft_major_holders.csv")
msft.institutional_holders.to_csv(f"data/{ticker}/msft_institutional_holders.csv")
msft.mutualfund_holders.to_csv(f"data/{ticker}/msft_mutualfund_holders.csv")


# save earnings dates to CSV
msft.earnings_dates.to_csv(f"data/{ticker}/msft_earnings_dates.csv")
