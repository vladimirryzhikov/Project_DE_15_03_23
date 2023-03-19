import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info (slow)
# print(msft.info)
# Returns a dictionary containing a wide range of information about the stock, such as its name, industry, sector, market cap, and more.

# fast access to subset of stock info (opportunistic)
print(msft.fast_info)
# Returns a smaller subset of the data in the `info` dictionary. This method can be faster than `info` but may not contain all of the data.

# get historical market data
hist = msft.history(period="1mo")
print(hist)
# Returns a pandas DataFrame containing historical price and volume data for the specified period.

# show meta information about the history (requires history() to be called first)
print(msft.history_metadata)
# Returns a dictionary containing metadata about the historical data
