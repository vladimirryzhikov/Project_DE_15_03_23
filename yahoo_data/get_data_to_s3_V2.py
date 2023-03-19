import yfinance as yf
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
import os


def get_sp500_tickers():
    """
    Retrieves a list of S&P 500 tickers from Wikipedia.

    Returns:
        A list of tickers.
    """
    sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    data_table = pd.read_html(sp500url)[0]
    tickers = data_table["Symbol"].tolist()
    return tickers


def get_ticker_data(ticker, start_date, end_date):
    """
    Retrieves historical stock data for a given ticker and time range.

    Args:
        ticker (str): The ticker symbol.
        start_date (str): The start date in "YYYY-MM-DD" format.
        end_date (str): The end date in "YYYY-MM-DD" format.

    Returns:
        A Pandas DataFrame containing the historical stock data.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def save_to_csv(data, path):
    """
    Saves a DataFrame to a CSV file.

    Args:
        data (pandas.DataFrame): The DataFrame to save.
        path (str): The path to save the CSV file to.
    """
    data.to_csv(path, index=False)


def upload_to_s3(file_path, bucket, s3_file_path):
    """
    Uploads a file to an S3 bucket.

    Args:
        file_path (str): The path to the file to upload.
        bucket (str): The name of the S3 bucket.
        s3_file_path (str): The path to store the file in the S3 bucket.
    """
    s3 = boto3.client("s3")
    try:
        s3.upload_file(file_path, bucket, s3_file_path)
        print(
            f"Successfully uploaded {file_path} to S3 bucket {bucket} as {s3_file_path}"
        )
    except FileNotFoundError:
        print(f"{file_path} not found.")
    except NoCredentialsError:
        print("Credentials not available.")


if __name__ == "__main__":
    tickers = get_sp500_tickers()
    start_date = "2022-03-01"
    end_date = "2022-03-03"
    s3_bucket_name = "bronzelayer"

    for ticker in tickers:
        data = get_ticker_data(ticker, start_date, end_date)
        file_path = f"data/{ticker}.csv"
        save_to_csv(data, file_path)
        upload_to_s3(file_path, s3_bucket_name, f"data/{ticker}.csv")
