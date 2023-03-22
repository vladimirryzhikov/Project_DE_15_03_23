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
logger_yfinance = logging.getLogger("yfinance")
logger_yfinance.setLevel(logging.DEBUG)

# Add console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger_yfinance.addHandler(ch)


s3_bucket = "bronzelayer"
s3_logs_folder = "logs/"

s3 = boto3.client("s3")


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
    except Exception as e:
        logger_yfinance.error(f"Error downloading data for {ticker}: {e}")
        return None


def main():
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()

    # Get the list of tickers
    tickers = tickers_table["Symbol"].tolist()

    # Loop over each ticker and download the historical data
    for ticker in tickers:
        data = download_data(ticker)
        if data is not None:
            s3_file = f"historical_data/{ticker}.csv"
            if upload_to_aws(data, s3_bucket, s3_file):
                logger.info(f"Uploaded data for {ticker} to S3")
            else:
                logger.warning(f"Failed to upload data for {ticker} to S3")


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
