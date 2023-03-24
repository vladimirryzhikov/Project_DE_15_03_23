import yfinance as yf
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import argparse
import logging
import datetime

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3_bucket = "bronzelayer"
s3_data_folder = "historical_data/"
s3_shares_folder = "shares_data/"
s3_earnings_folder = "earnings_data/"
s3_logs_folder = "logs/"

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


def retrieve_tickers():
    """Retrieves the list of all S&P500 stock market companies from Wikipedia"""
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    return data_table


def upload_to_aws(df, s3_bucket, s3_folder, s3_file):
    """Uploads a dataframe to an S3 bucket"""
    try:
        csv_buffer = df.to_csv(index=False)
        s3.put_object(Body=csv_buffer, Bucket=s3_bucket, Key=s3_folder + s3_file)
        logger.info(f"Data uploaded to S3 bucket: {s3_folder + s3_file}")
        return True
    except NoCredentialsError:
        logger.error("Credentials not available")
        return False


def download_data(ticker):
    """Downloads historical data for a given ticker"""
    try:
        data = yf.download(ticker, group_by="Ticker")
        data["ticker"] = ticker  # add the column ticker to dataframe
        logger.info(f"Downloaded data for {ticker}")
        return data
    except:
        logger.error(f"Error downloading data for {ticker}")
        return None


def download_shares_earnings(ticker):
    """Downloads shares and earnings data for a given ticker"""
    try:
        # Download the shares data
        shares = yf.Ticker(ticker).shares_outstanding.reset_index()
        shares.columns = ["Date", "Shares"]
        shares["ticker"] = ticker

        # Download the earnings data
        earnings = yf.Ticker(ticker).earnings.reset_index()
        earnings = earnings[["Date", "Earnings"]]
        earnings.columns = ["Date", "Earnings"]
        earnings["ticker"] = ticker

        logger.info(f"Downloaded shares and earnings data for {ticker}")
        return shares, earnings
    except:
        logger.error(f"Error downloading shares and earnings data for {ticker}")
        return None, None


def main():
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()

    # Get the list of tickers
    tickers = tickers_table["Symbol"].tolist()
    # Change the two elements of the list of tickers prior to wrong names
    tickers[tickers.index("BRK.B")] = "BRK-B"
    # tickers[tickers.index("BRK.H")] = "BRK-H"

    # Loop over each ticker and download the historical data, shares data, and earnings data
    for ticker in tickers:
        # Download historical data
        data = download_data(ticker)
        if data is not None:
            s3_file = f"historical_data/{ticker}.csv"
            if upload_to_aws(data, s3_bucket, s3_file):
                logger.info(f"Uploaded historical data for {ticker} to S3")
            else:
                logger.warning(f"Failed to upload historical data for {ticker} to S3")

        # Download shares data
        shares_data = yf.Ticker(ticker).get_shareholders()
        if shares_data is not None:
            shares_file = f"shares_data/{ticker}.csv"
            if upload_to_aws(shares_data, s3_bucket, shares_file):
                logger.info(f"Uploaded shares data for {ticker} to S3")
            else:
                logger.warning(f"Failed to upload shares data for {ticker} to S3")

        # Download earnings data
        earnings_data = yf.Ticker(ticker).earnings
        if not earnings_data.empty:
            earnings_file = f"earnings_data/{ticker}.csv"
            if upload_to_aws(earnings_data, s3_bucket, earnings_file):
                logger.info(f"Uploaded earnings data for {ticker} to S3")
            else:
                logger.warning(f"Failed to upload earnings data for {ticker} to S3")
