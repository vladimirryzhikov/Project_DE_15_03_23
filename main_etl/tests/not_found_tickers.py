import boto3
import pandas as pd

sp500url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
data_table = pd.read_html(sp500url)[0]


bucket_name = "testbucket"
directory_paths = ["earnings_data/", "historical_data/", "shares_data/"]
data_table.to_csv("tickers.csv", columns=["Symbol"], index=False)
tickers = data_table["Symbol"].tolist()


""" s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


not_found = []

for ticker in tickers:
    for path in directory_paths:
        file_name = path + ticker + ".csv"

        try:
            s3.head_object(Bucket=bucket_name, Key=file_name)
        except:
            not_found.append(ticker)
            with open("log/not_found.txt", "a") as f:
                f.write(f"{ticker}\n")

print("Not Found Tickers:", not_found)
 """
