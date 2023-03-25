import yfinance as yf
import pandas as pd

# List of tickers
tickers = ["AAPL", "GOOG", "TSLA"]

# Loop over each ticker and get the fast info dictionary
for ticker in tickers:
    fast_info = yf.Ticker(ticker)._fast_info

    # Check if the dictionary is not empty
    if fast_info.keys():
        # Convert the dictionary to a pandas dataframe
        df = pd.DataFrame(fast_info.items(), columns=["Attribute", "Value"])

        # Save the dataframe to a CSV file
        df.to_csv(f"{ticker}_fast_info.csv", index=False)
