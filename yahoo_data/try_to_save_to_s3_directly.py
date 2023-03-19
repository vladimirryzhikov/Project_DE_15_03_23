import io
import os

import boto3
import pandas as pd


AWS_S3_BUCKET = "bronzelayer"

s3_client = boto3.client("s3")

tickers_df = pd.read_csv("data/all_tickers.csv")

with io.StringIO() as csv_buffer:
    tickers_df.to_csv(csv_buffer, index=False)

    response = s3_client.put_object(
        Bucket=AWS_S3_BUCKET, Key="all_tickers.csv", Body=csv_buffer.getvalue()
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        print(f"Successful S3 put_object response. Status - {status}")
    else:
        print(f"Unsuccessful S3 put_object response. Status - {status}")
