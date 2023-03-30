import os
import yfinance as yf
import pandas as pd

data_folder = "data/"
tickers_file = "tickers.csv"
historical_data_folder = "historical_data/"
shares_folder = "shares/"
earnings_folder = "earnings/"


def retrieve_tickers():
    """Read the csv tickers file and get the list of tickers"""
    data_table = pd.read_csv(f"{data_folder}{tickers_file}")
    tickers_list = data_table["Symbol"].tolist()  # convert to list

    # Rename 2 tickers due to mistakes in Yahoo naming
    tickers_list[tickers_list.index("BRK.B")] = "BRK-B"
    tickers_list[tickers_list.index("BF.B")] = "BF-B"

    return tickers_list


def check_directory(ticker):
    """Check if ticker has files in all three directories"""
    if (
        os.path.exists(f"{data_folder}{historical_data_folder}{ticker}.csv")
        and os.path.exists(f"{data_folder}{shares_folder}{ticker}.csv")
        and os.path.exists(f"{data_folder}{earnings_folder}{ticker}.csv")
    ):
        return True
    else:
        return False


def delete_tickers_data(tickers):
    """Deleting the csv data files locally that not downloaded completly"""
    for ticker in tickers:
        for directory in [historical_data_folder, shares_folder, earnings_folder]:
            file_path = os.path.join(data_folder, directory, f"{ticker}.csv")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted {file_path}")


def main():
    # Retrieve the list of tickers
    tickers = retrieve_tickers()

    # Create a new list of tickers that have data in all three directories
    new_tickers = []
    for ticker in tickers:
        if check_directory(ticker):
            new_tickers.append(ticker)
        else:
            print(ticker)
    # Write the new list of tickers to a new tickers file
    df = pd.DataFrame({"Symbol": new_tickers})
    df.to_csv(f"{data_folder}new_{tickers_file}", index=False)
    delete_tickers_data(new_tickers)


if __name__ == "__main__":
    main()
