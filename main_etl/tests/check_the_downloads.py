import boto3
import pandas as pd

sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
data_table = pd.read_html(sp500url)[0]


bucket_name = "testbucket"
directory_paths = ["earnings_data/", "historical_data/", "shares_data/"]
tickers = data_table["Symbol"].tolist()


s3 = boto3.client("s3", endpoint_url="http://localhost:4566")
count = 0
for ticker in tickers:
    for path in directory_paths:
        file_name = path + ticker + ".csv"

        try:
            s3.head_object(Bucket=bucket_name, Key=file_name)
            print(f"{file_name} exists in {bucket_name}")
            count += 1
            print(f"Found {count} files")
        except:
            print(f"{file_name} does not exist in {bucket_name}")
