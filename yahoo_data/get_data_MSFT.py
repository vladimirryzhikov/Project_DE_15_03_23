import yfinance as yf
import os

ticker = "BRK-B"  # WORKING FUNCTIONS ODF DATA TICKER TESTED ON MSFT NEED TO LOOP OVER ALL TICKETS AND ADD THE CODE TO WORKING SCRIPT

# create the directory if it doesn't exist
if not os.path.exists(f"data/{ticker}"):
    os.makedirs(f"data/{ticker}")

# create Ticker object
msft = yf.Ticker(ticker)

# get historical market data and save to CSV
hist = msft.history(period="1mo")
hist.to_csv(f"data/{ticker}/msft_history.csv")

# save actions to CSV
msft.actions.to_csv(f"data/{ticker}/msft_actions.csv")
msft.dividends.to_csv(f"data/{ticker}msft_dividends.csv")
msft.splits.to_csv(f"data/{ticker}msft_splits.csv")

# save share count to CSV
msft.get_shares_full(start="2022-01-01", end=None).to_csv(
    f"data/{ticker}/msft_shares.csv"
)

# save financials to CSV
# print(msft.income_stmt) didint decrypt
# .to_csv(f"data/{ticker}/msft_income_stmt.csv")
""" msft.quarterly_income_stmt.to_txt(f"data/{ticker}/msft_quarterly_income_stmt.csv")
msft.balance_sheet.to_txt(f"data/{ticker}/msft_balance_sheet.csv")
msft.quarterly_balance_sheet.to_txt(f"data/{ticker}/msft_quarterly_balance_sheet.csv")
msft.cashflow.to_txt(f"data/{ticker}/msft_cashflow.csv")
msft.quarterly_cashflow.to_txt(f"data/{ticker}/msft_quarterly_cashflow.csv")
 """
# save holders to CSV
msft.major_holders.to_csv(f"data/{ticker}/msft_major_holders.csv")
msft.institutional_holders.to_csv(f"data/{ticker}/msft_institutional_holders.csv")
msft.mutualfund_holders.to_csv(f"data/{ticker}/msft_mutualfund_holders.csv")

# save earnings to CSV
# msft.earnings
# .to_txt(f"data/{ticker}/msft_earnings.csv")
# msft.quarterly_earnings
# .to_txt(f"data/{ticker}/msft_quarterly_earnings.csv")

# save sustainability to CSV
""" msft.sustainability.to_txt(f"data/{ticker}/msft_sustainability.csv")

# save analysts recommendations to CSV
msft.recommendations.to_txt(f"data/{ticker}/msft_recommendations.csv")
msft.recommendations_summary.to_txt(f"data/{ticker}/msft_recommendations_summary.csv")
msft.analyst_price_target.to_txt(f"data/{ticker}/msft_analyst_price_target.csv")
msft.revenue_forecasts.to_txt(f"data/{ticker}/msft_revenue_forecasts.csv")
msft.earnings_forecasts.to_txt(f"data/{ticker}/msft_earnings_forecasts.csv")
msft.earnings_trend.to_txt(f"data/{ticker}/msft_earnings_trend.csv")

# save next event to CSV
msft.calendar.to_txt(f"data/{ticker}/msft_calendar.csv")
 """
# save earnings dates to CSV
msft.earnings_dates.to_csv(f"data/{ticker}/msft_earnings_dates.csv")

# save ISIN code to CSV
# msft.isin.to_txt(f"data/{ticker}/msft_isin.csv")

# save options expirations to CSV
# msft.options.to_txt(f"data/{ticker}/msft_options.csv")

# save news to CSV
# print(msft.news)
