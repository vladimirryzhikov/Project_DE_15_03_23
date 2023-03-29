import os
import csv
import yfinance as yf
import pandas as pd
from datetime import datetime

# Set the data folder path and tickers file name
data_folder = "data/"
tickers_file = "tickers.csv"

# Create a directory with today's date to store the CSV files
today_dir = f"{data_folder}{datetime.today().strftime('%Y-%m-%d')}/"
os.makedirs(today_dir, exist_ok=True)


# Retrieve the tickers list
def retrieve_tickers():
    """Read the csv tickers file and get the list of tickers"""
    data_table = pd.read_csv(f"{data_folder}{tickers_file}")
    tickers_list = data_table["Symbol"].tolist()  # convert to list
    return tickers_list


# Loop over the tickers and get their fast info data
for ticker in retrieve_tickers():
    # Get the fast info dictionary for the ticker
    fast_info = yf.Ticker(ticker)._fast_info

    # Create a CSV file for writing
    with open(f"{today_dir}{ticker}_fast_info.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(["Attribute", "Value"])

        # Loop over the dictionary and write each row to the CSV file
        for key, value in fast_info.items():
            writer.writerow([key, value])

print("Done.")
