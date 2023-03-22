import yfinance as yf
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import argparse


# need to add creation bucket check and set parametrized
def retrieve_tickers():
    """Retrieves the list of all S&P500 stock market companies from Wikipedia"""
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    return data_table


def upload_to_aws(df, s3_bucket, s3_file):
    """Uploads a dataframe to an S3 bucket"""
    s3 = boto3.client("s3")
    try:
        csv_buffer = df.to_csv(index=False)
        s3.put_object(Body=csv_buffer, Bucket=s3_bucket, Key=s3_file)
        print(f"Data uploaded to S3 bucket: {s3_file}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


def download_data(ticker):
    """Downloads historical data for a given ticker"""
    try:
        data = yf.download(ticker, group_by="Ticker")
        data["ticker"] = ticker  # add the column ticker to dataframe
        return data
    except:
        print(f"Error downloading data for {ticker}")
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
            s3_bucket = "bronzelayer"
            s3_file = f"historical_data/{ticker}.csv"
            upload_to_aws(data, s3_bucket, s3_file)


if __name__ == "__main__":
    main()
