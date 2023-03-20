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


def download_data(ticker, start_date, end_date):
    """Downloads historical data for a given ticker and date range"""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        data["ticker"] = ticker  # add the column ticker to dataframe
        return data
    except:
        print(f"Error downloading data for {ticker}")
        return None


def main(start_date="2012-01-01", end_date="2022-01-01"):
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()

    # Get the list of tickers
    tickers = tickers_table["Symbol"].tolist()

    # Set the date range for the data
    # start_date = "2022-02-01"
    # end_date = "2022-02-10"

    # Loop over each ticker and download the historical data
    for ticker in tickers:
        data = download_data(ticker, start_date, end_date)
        if data is not None:
            s3_bucket = "bronzelayer"
            s3_file = f"historical_data/{ticker}.csv"
            upload_to_aws(data, s3_bucket, s3_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "start_date",
        type=str,
        default="2012-01-01",
        help="Start date to start history data",
    )
    parser.add_argument(
        "end_date",
        type=str,
        default="2022-01-01",
        help="End date to end history data< we will get 10 years",
    )
    args = parser.parse_args()
    main(args.start_date, args.end_date)
