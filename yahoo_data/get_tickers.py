import pandas as pd


def get_sp500_tickers():
    """
    Retrieves a list of S&P 500 tickers from Wikipedia.

    Returns:
        A list of tickers.
    """
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    data_table.to_csv("data/all_tickers.csv", index=False)
    tickers = data_table["Symbol"].tolist()
    return tickers


if __name__ == "__main__":
    tickers = get_sp500_tickers()
    tickers_df = pd.DataFrame({"tickers": tickers})
    tickers_df.to_csv("data/sp500_tickers.csv", index=False)
