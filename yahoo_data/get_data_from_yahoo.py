import yfinance as yf

# Define the ticker symbol
ticker = "BF-B"

# Get data for the past 5 years
start_date = "2016-01-01"
end_date = "2021-12-31"

# Get the data
data = yf.download(ticker, group_by="Ticker")

# Print the data
print(type(data))
print(data.columns)
print(data)
