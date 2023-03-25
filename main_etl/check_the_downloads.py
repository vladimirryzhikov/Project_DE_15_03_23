import os
import pandas as pd

# Define the tickers and data folders

data_folders = ["data/shares/", "data/historical_data/", "data/earnings/"]
tickers = pd.read_csv("data/tickers.csv")
tickers_list = tickers["Symbol"].tolist()  # convert to list
# Check if each file exists in its respective folder
results = []
for ticker in tickers_list:
    for folder in data_folders:
        file_path = f"{folder}{ticker}.csv"
        if not os.path.isfile(file_path):
            results.append(f"{ticker} data missing in {folder}\n")
if not results:
    results.append("All data downloaded successfully!")

# Save the results to a file
with open("download_check.txt", "w") as f:
    f.writelines(results)

# Print the results to the console
print("".join(results))
