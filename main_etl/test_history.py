import yfinance as yf
import pandas as pd


data_folder = "data/"
tickers_file = "tickers.csv"
historical_data_folder = "historical_data/"
shares_folder = "shares/"
earnings_folder = "earnings/"

tickers = ["AAPL"]


for ticker in tickers:
    data = yf.download(ticker, group_by="Ticker")
    data["ticker"] = ticker  # add the column 'ticker' to dataframe
    print(data)
    data.to_csv(f"{data_folder}{historical_data_folder}{ticker}.csv", index=True)

    """ shares = yf.Ticker(ticker).get_shares_full(start="2022-01-01", end=None)

    shares.columns = ["Date", "Shares", "Ticker"]
    shares["Ticker"] = ticker """

    # Download the earnings data
    # earnings = yf.Ticker(ticker).earnings_dates()
    # earnings = earnings[["Date", "Earnings"]]
    # earnings.columns = ["Date", "Earnings"]
    # earnings["ticker"] = ticker
    """ print(shares)
    shares.to_csv(f"{data_folder}{shares_folder}{ticker}.csv", index=True) """
    # earnings = yf.Ticker(ticker).earnings_dates
    # earnings = earnings[["Date", "Earnings"]]
    # earnings.columns = ["Date", "Earnings"]
    # earnings["ticker"] = ticker
    # earnings.to_csv(f"{data_folder}{earnings_folder}{ticker}.csv")
    # print(earnings)

    """ test = yf.Ticker(ticker).actions
    print(test) """
# bf.b to test
