import yfinance as yf

tickers = ["ANET", "FOX", "IBM", "NWS", "NVDA"]

results = []

for ticker in tickers:
    # Check if the ticker exists in Yahoo Finance
    """try:
        yf.download(ticker, group_by="Ticker")
    except:
        results.append(f"{ticker} ticker not found in Yahoo Finance database")
        continue"""

    # Check if the data is available for the specified period
    shares = yf.Ticker(ticker).get_shares_full(start="2000-01-01", end=None)
    if shares.empty:
        results.append(f"{ticker} shares data not available for the specified period")

    earnings = yf.Ticker(ticker).earnings_dates
    if earnings.empty:
        results.append(f"{ticker} earnings data not available")


if len(results) == 0:
    results.append("All data downloaded successfully for all tickers")

with open("data_check_results.txt", "w") as f:
    f.write("\n".join(results))
