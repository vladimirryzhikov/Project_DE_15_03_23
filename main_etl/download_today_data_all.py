import yfinance as yf
import pandas as pd
import os
from datetime import datetime


data_folder = "data/"
tickers_file = "tickers.csv"
# Define the list of tickers to download data for
data_table = pd.read_csv(f"{data_folder}{tickers_file}")
tickers_list = data_table["Symbol"].tolist()  # convert to list


# Create a folder to store the data for today's date
today_dir = f"{data_folder}{datetime.today().strftime('%Y-%m-%d')}/"
os.makedirs(today_dir, exist_ok=True)

if not os.path.exists(data_folder):
    os.mkdir(data_folder)

# Loop over each ticker in the list and download the data
for ticker in tickers_list:
    try:
        # Download the data using yfinance
        data = yf.Ticker(ticker).history(period="1d")

        # Save the data to a CSV file in the today_folder directory
        filename = f"{today_dir}/{ticker}.csv"
        data.to_csv(filename)

        print(f"Data downloaded for {ticker}")
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
