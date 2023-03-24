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

s3_bucket = "testbucket"
s3_logs_folder = "logs/"

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

# in that function we need to apply some min transformation
# prior to the different names for two tickers BRK.b -> BRK-B and BRK.H -> BRK-H


def retrieve_tickers():
    """Retrieves the list of all S&P500 stock market companies from Wikipedia"""
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    return data_table


def upload_to_aws(df, s3_bucket, s3_file):
    """Uploads a dataframe to an S3 bucket"""
    try:
        csv_buffer = df.to_csv()
        s3.put_object(Body=csv_buffer, Bucket=s3_bucket, Key=s3_file)
        logger.info(f"Data uploaded to S3 bucket: {s3_file}")
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


def download_shares(ticker):
    """Downloads shares data for a given ticker"""
    try:
        # Download the shares data
        shares = yf.Ticker(ticker).get_shares_full(start="2022-01-01", end=None)
        # shares.columns = ["Date", "Shares"]
        # shares["ticker"] = ticker

        # Download the earnings data
        # earnings = yf.Ticker(ticker).earnings_dates()
        # earnings = earnings[["Date", "Earnings"]]
        # earnings.columns = ["Date", "Earnings"]
        # earnings["ticker"] = ticker

        # Concatenate the shares and earnings dataframes
        # data = pd.concat([shares, earnings], axis=1)
        logger.info(f"Downloaded shares and earnings data for {ticker}")
        return shares
    except:
        logger.error(f"Error downloading shares and earnings data for {ticker}")
        return None


def download_earnings(ticker):
    """Downloads earnings data for a given ticker"""
    try:
        # Download the earnings data
        earnings = yf.Ticker(ticker).earnings_dates
        # earnings = earnings[["Date", "Earnings"]]
        # earnings.columns = ["Date", "Earnings"]
        # earnings["ticker"] = ticker

        logger.info(f"Downloaded earnings data for {ticker}")
        return earnings
    except:
        logger.error(f"Error downloading earnings data for {ticker}")
        return None


def main():
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()

    # Get the list of tickers
    # tickers = tickers_table["Symbol"].tolist()
    # Test script with 3 tickers
    tickers = ["AAPL", "MSFT", "BRK-B"]
    # Change the two elements of the list of tickers prior to wrong names

    # tickers[tickers.index("BRK.B")] = "BRK-B"

    # Loop over each ticker and download the historical data
    for ticker in tickers:
        data = download_data(ticker)
        if data is not None:
            s3_file = f"historical_data/{ticker}.csv"
            if upload_to_aws(data, s3_bucket, s3_file):
                logger.info(f"Uploaded data for {ticker} to S3")
            else:
                logger.warning(f"Failed to upload data for {ticker} to S3")

            # Download shares data
            shares_data = download_shares(ticker)
            if shares_data is not None:
                s3_file = f"shares_data/{ticker}.csv"
                if upload_to_aws(shares_data, s3_bucket, s3_file):
                    logger.info(f"Uploaded shares data for {ticker} to S3")
                else:
                    logger.warning(f"Failed to upload shares data for {ticker} to S3")

            # Download earnings data
            earnings_data = download_earnings(ticker)
            if earnings_data is not None:
                s3_file = f"earnings_data/{ticker}.csv"
                if upload_to_aws(earnings_data, s3_bucket, s3_file):
                    logger.info(f"Uploaded shares and earnings data for {ticker} to S3")
                else:
                    logger.warning(
                        f"Failed to upload shares and earnings data for {ticker} to S3"
                    )


if __name__ == "__main__":
    # Set up logging to file
    log_file_name = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".log"
    file_handler = logging.FileHandler(s3_logs_folder + log_file_name)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Set up logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    main()
    # Upload logs to S3
    upload_to_aws(
        pd.read_csv(s3_logs_folder + log_file_name),
        s3_bucket,
        s3_logs_folder + log_file_name,
    )
