import pandas as pd

data_folder = "data/"


def retrieve_tickers():
    """Retrieves the list of all S&P500 stock market companies from Wikipedia"""
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    return data_table


def save_tickers(tickers, filename):
    """Saves the list of tickers to a CSV file"""
    tickers.to_csv(filename, index=False)


def main():
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()
    save_tickers(tickers_table, f"{data_folder}all_tickers.csv")
    save_tickers(tickers_table["Symbol"], f"{data_folder}tickers.csv")


if __name__ == "__main__":
    main()
