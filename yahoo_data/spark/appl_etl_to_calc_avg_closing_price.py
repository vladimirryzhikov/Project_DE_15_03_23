import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# from moto import mock_s3, mock_sts
import boto3

# from localstack import config
# from localstack.services import infra
# from localstack.services.s3 import s3_listener

# Set environment variables required for Spark to find the Spark installation directory
# os.environ['SPARK_HOME'] = '/path/to/spark'
# os.environ['PYSPARK_PYTHON'] = '/path/to/python'

# Create a Spark session
spark = SparkSession.builder.appName("local-spark-job").getOrCreate()

# Start Localstack services
# infra.start_infra(asynchronous=True)


# Mock S3 and STS services using Moto
# @mock_s3
# @mock_sts
def main():
    # Create the S3 bucket
    s3_client = boto3.client("s3", endpoint_url="http://localhost:4566")
    s3_bucket = "bronzelayer"
    s3_new_bucket = "silverlayer"
    region = "eu-north-1"
    s3_client.create_bucket(
        Bucket=s3_new_bucket, CreateBucketConfiguration={"LocationConstraint": region}
    )

    # Upload the CSV files to the S3 bucket
    ticker = "ABBV"
    # s3_folder_path = f's3://{s3_bucket}/{ticker}/'
    s3_folder_path = f"s3://{s3_bucket}/historical_data/"
    s3_file_path = s3_folder_path + f"{ticker}.csv"
    s3_shares_path = s3_folder_path + f"{ticker}_shares.csv"
    s3_earnings_path = s3_folder_path + f"{ticker}_earnings.csv"
    need to download all data shares earnings etc !!!!
    s3_client.upload_file("path/to/csv/file", s3_bucket, s3_file_path)
    s3_client.upload_file("path/to/csv/file", s3_bucket, s3_shares_path)
    s3_client.upload_file("path/to/csv/file", s3_bucket, s3_earnings_path)

    # Read the CSV files using Spark
    df = spark.read.csv(s3_file_path, header=True, inferSchema=True)

    # Load the shares data and join it with the main data frame
    shares_df = spark.read.csv(s3_shares_path, header=True, inferSchema=True)
    df = df.join(shares_df, on=["Date"])

    # group the data by year and calculate the average closing price
    df = (
        df.withColumn("year", year("Date"))
        .groupBy("year")
        .agg(avg("Close").alias("average_close"))
    )

    # write the transformed data to a new S3 bucket
    s3_output_path = f"s3://{s3_new_bucket}/{ticker}_output/"
    df.write.mode("overwrite").option("header", "true").csv(s3_output_path)


if __name__ == "__main__":
    main()
