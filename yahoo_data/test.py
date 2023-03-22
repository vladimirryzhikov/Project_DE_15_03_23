import yfinance as yf
import os
import logging

# set up logging
logging.basicConfig(
    filename="data_retrieval.log",
    level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


# list of tickers to get data for
tickers = ["AAPL", "MSFT", "GOOG", "BRK-B", "BRK.H"]

for ticker in tickers:
    try:
        # create the directory if it doesn't exist
        if not os.path.exists(f"data/{ticker}"):
            os.makedirs(f"data/{ticker}")

        # create Ticker object
        t = yf.Ticker(ticker)

        # get historical market data and save to CSV
        hist = t.history()
        hist["Ticker"] = ticker
        if not hist.empty:
            hist.to_csv(f"data/{ticker}/{ticker}_history.csv")

        # save actions to CSV
        actions = t.actions
        actions["Ticker"] = ticker
        if not actions.empty:
            actions.to_csv(f"data/{ticker}/{ticker}_actions.csv")

        dividends = t.dividends
        dividends["Ticker"] = ticker
        if not dividends.empty:
            dividends.to_csv(f"data/{ticker}/{ticker}_dividends.csv")

        splits = t.splits
        splits["Ticker"] = ticker
        if not splits.empty:
            splits.to_csv(f"data/{ticker}/{ticker}_splits.csv")

        # save share count to CSV
        shares = t.get_shares_full(start="2022-01-01", end=None)
        shares["Ticker"] = ticker
        if not shares.empty:
            shares.to_csv(f"data/{ticker}/{ticker}_shares.csv")

        # save holders to CSV
        major_holders = t.major_holders
        major_holders["Ticker"] = ticker
        if not major_holders.empty:
            major_holders.to_csv(f"data/{ticker}/{ticker}_major_holders.csv")

        institutional_holders = t.institutional_holders
        institutional_holders["Ticker"] = ticker
        if not institutional_holders.empty:
            institutional_holders.to_csv(
                f"data/{ticker}/{ticker}_institutional_holders.csv"
            )

        mutualfund_holders = t.mutualfund_holders
        mutualfund_holders["Ticker"] = ticker
        if not mutualfund_holders.empty:
            mutualfund_holders.to_csv(f"data/{ticker}/{ticker}_mutualfund_holders.csv")

        # save earnings dates to CSV
        earnings_dates = t.earnings_dates
        earnings_dates["Ticker"] = ticker
        if not earnings_dates.empty:
            earnings_dates.to_csv(f"data/{ticker}/{ticker}_earnings_dates.csv")

    except Exception as e:
        logging.error(f"Error occurred while retrieving data for {ticker}: {e}")
