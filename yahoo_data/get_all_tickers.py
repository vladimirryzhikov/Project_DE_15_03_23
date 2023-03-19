import yfinance as yf
import pandas as pd


def retrieve_tickers():
    """Retrieves the list of all S&P500 stock market companies from Wikipedia"""
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    return data_table


def save_tickers(tickers, filename):
    """Saves the list of tickers to a CSV file"""
    tickers.to_csv(filename, columns=["Symbol"], index=False)


def download_data(ticker, start_date, end_date):
    """Downloads historical data for a given ticker and date range"""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        data.to_csv(f"{ticker}.csv", index=False)
        print(f"Downloaded data for {ticker}")
    except:
        print(f"Error downloading data for {ticker}")


def main():
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()
    save_tickers(tickers_table, "all_tickers.csv")
    save_tickers(tickers_table["Symbol"], "tickers.csv")

    # Get the list of tickers
    tickers = tickers_table["Symbol"].tolist()

    # Set the date range for the data
    start_date = "2000-01-01"
    end_date = "2022-03-18"

    # Loop over each ticker and download the historical data
    for ticker in tickers:
        download_data(ticker, start_date, end_date)


if __name__ == "__main__":
    main()
