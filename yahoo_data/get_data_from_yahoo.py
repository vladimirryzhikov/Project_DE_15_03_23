import yfinance as yf

# Define the ticker symbol
tickerSymbol = "AAPL"

# Get data for the past 5 years
start_date = "2016-01-01"
end_date = "2021-12-31"

# Get the data
data = yf.download(tickerSymbol, start=start_date, end=end_date)

# Print the data
print(type(data))
# print(data.columns)
