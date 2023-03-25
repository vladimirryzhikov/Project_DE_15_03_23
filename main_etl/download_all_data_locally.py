import yfinance as yf
import pandas as pd


data_folder = "data/"
tickers_file = "tickers.csv"
historical_data_folder = "historical_data/"
shares_folder = "shares/"
earnings_folder = "earnings/"


# need to add creation bucket check and set parametrized
def retrieve_tickers():
    """Read the csv tickers file and get the list of tickers"""
    data_table = pd.read_csv(f"{data_folder}{tickers_file}")
    tickers_list = data_table["Symbol"].tolist()  # convert to list
    return tickers_list


def download_data(ticker):
    """Downloads historical data for a given ticker and date range"""
    try:
        data = yf.download(ticker, group_by="Ticker")
        data["ticker"] = ticker  # add the colukn ticker to dataframe
        data.to_csv(f"{data_folder}{historical_data_folder}{ticker}.csv", index=True)
        print(f"Downloaded data for {ticker}")
        return True
    except:
        print(f"Error downloading data for {ticker}")
        return False


def download_shares(ticker):
    """Downloads shares data for a given ticker"""
    try:
        # Download the shares data
        shares = yf.Ticker(ticker).get_shares_full(start="2022-01-01", end=None)

        shares.to_csv(f"{data_folder}{shares_folder}{ticker}.csv", index=True)
        # shares.columns = ["Date", "Shares"]
        # shares["ticker"] = ticker

        # Download the earnings data
        # earnings = yf.Ticker(ticker).earnings_dates()
        # earnings = earnings[["Date", "Earnings"]]
        # earnings.columns = ["Date", "Earnings"]
        # earnings["ticker"] = ticker

        # Concatenate the shares and earnings dataframes
        # data = pd.concat([shares, earnings], axis=1)
        print(f"Downloaded shares data for {ticker}")
        return shares
    except:
        print(f"Error downloading shares data for {ticker}")
        return None


def download_earnings(ticker):
    """Downloads earnings data for a given ticker"""
    try:
        # Download the earnings data
        earnings = yf.Ticker(ticker).earnings_dates
        # earnings = earnings[["Date", "Earnings"]]
        # earnings.columns = ["Date", "Earnings"]
        # earnings["ticker"] = ticker
        earnings.to_csv(f"{data_folder}{earnings_folder}{ticker}.csv")
        print(f"Downloaded earnings data for {ticker}")
        return earnings
    except:
        print(f"Error downloading earnings data for {ticker}")
        return None


def main(start_date="2012-01-01", end_date="2022-01-01"):
    # Retrieve the list of tickers
    tickers = retrieve_tickers()
    tickers[
        tickers.index("BRK.B")
    ] = "BRK-B"  # the name for that ticker in yahoo is BRK-B
    # Set the date range for the data
    # start_date = "2022-02-01"
    # end_date = "2022-02-10"
    count_h = 0
    count_sh = 0
    count_e = 0
    # Loop over each ticker and download the historical data
    for ticker in tickers:
        data = download_data(ticker)
        if data is not None:
            print(
                f"Downloaded data for {ticker} to {data_folder}{historical_data_folder}"
            )
        else:
            print(
                f"Failed to Download data for {ticker} to {data_folder}{historical_data_folder}"
            )

            # Download shares data
        shares_data = download_shares(ticker)
        if shares_data is not None:
            print(f"Downloaded shares data for {ticker} {data_folder}{shares_folder}")
        else:
            print(
                f"Failed to Download shares data for {ticker} to {data_folder}{shares_folder}"
            )

            # Download earnings data
        earnings_data = download_earnings(ticker)
        if earnings_data is not None:
            print(
                f"Downloaded earnings data for {ticker} to {data_folder}{earnings_folder}"
            )
        else:
            print(
                f"Failed to Download and earnings data for {ticker} to {data_folder}{earnings_folder}"
            )


if __name__ == "__main__":
    main()
