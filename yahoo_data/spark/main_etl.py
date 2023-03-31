import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    DateType,
    LongType,
)


def create_spark_session():
    """
    Creates a Spark session with configurations for connecting to S3 and Localstack.
    """
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

    # Configure Spark for Localstack S3
    spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://127.0.0.1:4566")
    spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")

    return spark


def load_historical_data(spark, source_bucket, ticker):
    """
    Loads the historical stock data from an S3 bucket and returns a dataframe.
    """
    s3_historical_folder_path = f"s3a://{source_bucket}/data/historical_data/"
    s3_file_path = s3_historical_folder_path + f"{ticker}.csv"

    # Define the schema for the historical data dataframe
    schema_history = StructType(
        [
            StructField("Date", DateType()),
            StructField("Open", DoubleType()),
            StructField("High", DoubleType()),
            StructField("Low", DoubleType()),
            StructField("Close", DoubleType()),
            StructField("Adj Close", DoubleType()),
            StructField("Volume", LongType()),
            StructField("ticker", StringType()),
        ]
    )

    # Load the historical data from S3
    historical_df = spark.read.csv(s3_file_path, header=True, schema=schema_history)

    # Convert the date column to DateType
    historical_df = historical_df.withColumn("Date", to_date("Date", "yyyy-MM-dd"))

    return historical_df


def load_shares_data(spark, source_bucket, ticker):
    """
    Loads the shares outstanding data from an S3 bucket and returns a dataframe.
    """
    s3_shares_folder_path = f"s3a://{source_bucket}/data/shares/"
    s3_shares_path = s3_shares_folder_path + f"{ticker}.csv"

    # Define the schema for the shares dataframe
    schema_shares = StructType(
        [StructField("Date", DateType()), StructField("Shares", LongType())]
    )

    # Load the shares data from S3
    shares_df = spark.read.csv(s3_shares_path, header=False, schema=schema_shares)

    # Convert the date column to DateType
    shares_df = shares_df.withColumn("Date", to_date("Date", "yyyy-MM-dd"))

    return shares_df


def load_earnings_data(spark, source_bucket, ticker):
    """Loads the earnings data from s3 bucket and return a dataframe"""

    s3_earnings_folder_path = f"s3a://{source_bucket}/data/earnings/"
    s3_earnings_path = s3_earnings_folder_path + f"{ticker}.csv"

    # Define the schema for the earnings dataframe
    schema_earnings = StructType(
        [
            StructField("Earnings Date", DateType()),
            StructField("EPS Estimate", DoubleType()),
            StructField("Reported EPS", DoubleType()),
            StructField("Surprise(%)", DoubleType()),
        ]
    )
    # Load the earnings data from s3
    earnings_df = spark.read.csv(s3_earnings_path, header=True, schema=schema_earnings)
    # Convert the date column to DateType
    earnings_df = earnings_df.withColumn(
        "Earnings Date", to_date("Earnings Date", "yyyy-MM-dd")
    )
    # Droping
    earnings_df = earnings_df.drop("EPS Estimate", "Surprise(%)")

    return earnings_df


def calculate_average_close_price(df):
    """
    Calculates the average closing price for each year and returns a dataframe.
    """
    # Extract the year from the date column
    df = df.withColumn("Year", year("Date"))

    # Group by year and calculate the average closing price
    avg_close_df = (
        df.groupBy("Year").agg(avg("Close").alias("Avg Close")).orderBy("Year")
    )

    return avg_close_df


def calculate_market_cap(df):
    """Calculates the market cap for each day"""
    df = df.withColumn("Market Cap", col("Shares").cast("double") * col("Close"))
    # format the market cap column
    market_cup = df.withColumn("Market Cap", format_number(col("Market Cap"), 2))
    return market_cup


def main():
    # Define the S3 bucket and ticker for the data to be loaded
    source_bucket = "bronzelayer"
    destination_bucket = "silverlayer"
    ticker = "MSFT"

    # Create the Spark session
    spark = create_spark_session()

    # Load the historical data and shares data and earnings data
    historical_df = load_historical_data(spark, source_bucket, ticker)
    shares_df = load_shares_data(spark, source_bucket, ticker)
    earnings_df = load_earnings_data(spark, source_bucket, ticker)
    # Join the historical and shares dataframes on the date column
    joined_df = historical_df.join(shares_df, "Date")

    # Calculate the average closing price for each year
    avg_close_df = calculate_average_close_price(joined_df)

    # Define the S3 output path for the results
    # s3_output_path = f"s3a://{destination_bucket}/output/{ticker}_avg_close.parquet"

    # Write the results to S3 as a Parquet file
    # avg_close_df.write.mode("overwrite").parquet(s3_output_path)

    # testing not to production
    # joined_df = joined_df.drop("Open", "High", "Low", "Adj Close")

    joined_df = calculate_market_cap(joined_df)
    joined_df.show(joined_df.count(), False)
    print(joined_df.count())
    avg_close_df.show()
    earnings_df.show()


if __name__ == "__main__":
    main()
