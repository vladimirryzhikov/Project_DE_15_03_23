import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType,
    DateType,
    LongType,
)
import boto3


def main():
    # Create a Spark session
    spark = (
        SparkSession.builder.appName("local-spark-job")
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2")
        .getOrCreate()
    )

    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("fs.s3a.access.key", "test")
    hadoop_conf.set("fs.s3a.secret.key", "test")
    hadoop_conf.set("mapreduce.fileoutputcommitter.algorithm.version", "2")
    spark.conf.set("spark.sql.shuffle.partitions", "1")
    # configure spark for localstack s3
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://127.0.0.1:4566")
    spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")

    # Get the S3 source and destination buckets
    source_bucket = "bronzelayer"
    destination_bucket = "silverlayer"

    ticker = "AAPL"
    # s3_folder_path = f's3://{source_bucket}/{ticker}/'
    s3_historical_folder_path = f"s3a://{source_bucket}/data/historical_data/"
    s3_file_path = s3_historical_folder_path + f"{ticker}.csv"
    s3_shares_folder_path = f"s3a://{source_bucket}/data/shares/"
    s3_shares_path = s3_shares_folder_path + f"{ticker}.csv"
    s3_earnings_folder_path = f"s3a://{source_bucket}/data/earnings/"
    s3_earnings_path = s3_earnings_folder_path + f"{ticker}.csv"
    #!!!need to download all data shares earnings etc !!!!

    # Define the schema for the historical data dataframe
    schema_history = StructType(
        [
            StructField("Date", DateType()),
            StructField("Open", DoubleType()),
            StructField("High", DoubleType()),
            StructField("Low", DoubleType()),
            StructField("Close", DoubleType()),
            StructField("Adj Close", DoubleType()),
            StructField("Volume", IntegerType()),
            StructField("ticker", StringType()),
        ]
    )

    # Define the schema for the shares dataframe
    schema_shares = StructType(
        [StructField("Date", DateType()), StructField("Shares", LongType())]
    )

    # Read the history data
    historical_df = spark.read.csv(s3_file_path, header=True, schema=schema_history)

    shares_df = spark.read.csv(s3_shares_path, header=False, schema=schema_shares)
    shares_df = shares_df.withColumn("Date", to_date("Date", "yyyy-MM-dd"))
    df = historical_df.join(shares_df, on=["Date"])
    df.show()
    # Group the data by year and calculate the average closing price
    df = (
        df.withColumn("year", year("Date"))
        .groupBy("year")
        .agg(avg("Close").alias("average_close"))
    )

    # Show the results

    df.show()
    # write the transformed data to a new S3 bucket
    """ s3_output_path = f"s3a://{destination_bucket}/{ticker}_output/"
    df.write.mode("overwrite").option("header", "true").csv(s3_output_path) """


if __name__ == "__main__":
    main()
