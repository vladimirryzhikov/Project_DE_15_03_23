import yfinance as yf
import os
import logging
import pandas as pd

# set up logging
logging.basicConfig(
    filename="data_retrieval.log",
    level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


# define list of tickers to retrieve data for
"""Retrieves the list of all S&P500 stock market companies from Wikipedia"""
sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
data_table = pd.read_html(sp500url)[0]


tickers = data_table["Symbol"].tolist()

# loop over tickers and retrieve data
for ticker in tickers:
    try:
        # create the directory if it doesn't exist
        if not os.path.exists(f"data/{ticker}"):
            os.makedirs(f"data/{ticker}")

        # create Ticker object
        t = yf.Ticker(ticker)

        # get historical market data and save to CSV
        hist = t.history(period="1mo")
        hist.to_csv(f"data/{ticker}/{ticker}_history.csv")

        # save actions to CSV
        t.actions.to_csv(f"data/{ticker}/{ticker}_actions.csv")
        t.dividends.to_csv(f"data/{ticker}/{ticker}_dividends.csv")
        t.splits.to_csv(f"data/{ticker}/{ticker}_splits.csv")

        # save share count to CSV
        t.get_shares_full(start="2022-01-01", end=None).to_csv(
            f"data/{ticker}/{ticker}_shares.csv"
        )

        # save holders to CSV
        t.major_holders.to_csv(f"data/{ticker}/{ticker}_major_holders.csv")
        t.institutional_holders.to_csv(
            f"data/{ticker}/{ticker}_institutional_holders.csv"
        )
        t.mutualfund_holders.to_csv(f"data/{ticker}/{ticker}_mutualfund_holders.csv")

        # save earnings dates to CSV
        t.earnings_dates.to_csv(f"data/{ticker}/{ticker}_earnings_dates.csv")

    except Exception as e:
        logging.error(f"Error occurred while retrieving data for {ticker}: {e}")
