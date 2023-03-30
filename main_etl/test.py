import pandas as pd

data_folder = "data/"
tickers_file = "tickers.csv"

data_table = pd.read_csv(f"{data_folder}{tickers_file}")
tickers_list = data_table["Symbol"].tolist()  # convert to list

# Rename 2 tickers due to mistakes in Yahoo naming
tickers_list[tickers_list.index("BRK.B")] = "BRK-B"
tickers_list[tickers_list.index("BF.B")] = "BF-B"

print(tickers_list)
