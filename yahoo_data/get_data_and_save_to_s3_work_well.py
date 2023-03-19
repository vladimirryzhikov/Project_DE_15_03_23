import yfinance as yf
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError


# need to add creation bucket check and set parametrized
def retrieve_tickers():
    """Retrieves the list of all S&P500 stock market companies from Wikipedia"""
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    return data_table


def save_tickers(tickers, filename):
    """Saves the list of tickers to a CSV file"""
    tickers.to_csv(filename, columns=["Symbol"], index=False)


def download_data(ticker, start_date, end_date):
    """Downloads historical data for a given ticker and date range"""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        data.to_csv(f"{ticker}.csv", index=False)
        print(f"Downloaded data for {ticker}")
        return True
    except:
        print(f"Error downloading data for {ticker}")
        return False


def upload_to_aws(local_file, s3_bucket, s3_file):
    """Uploads a file to an S3 bucket"""
    s3 = boto3.client("s3")
    try:
        s3.upload_file(local_file, s3_bucket, s3_file)
        print(f"File uploaded to S3 bucket: {s3_file}")
        return True
    except FileNotFoundError:
        print(f"{local_file} not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def main():
    # Retrieve the list of tickers
    tickers_table = retrieve_tickers()
    save_tickers(tickers_table, "all_tickers.csv")
    save_tickers(tickers_table["Symbol"], "tickers.csv")

    # Upload the tickers files to S3
    upload_to_aws("all_tickers.csv", "bronzelayer", "all_tickers.csv")
    upload_to_aws("tickers.csv", "bronzelayer", "tickers.csv")

    # Get the list of tickers
    tickers = tickers_table["Symbol"].tolist()

    # Set the date range for the data
    start_date = "2022-02-01"
    end_date = "2022-02-10"

    # Loop over each ticker and download the historical data
    for ticker in tickers:
        if download_data(ticker, start_date, end_date):
            local_file = f"{ticker}.csv"
            s3_bucket = "bronzelayer"
            s3_file = f"historical_data/{ticker}.csv"
            upload_to_aws(local_file, s3_bucket, s3_file)


if __name__ == "__main__":
    main()
