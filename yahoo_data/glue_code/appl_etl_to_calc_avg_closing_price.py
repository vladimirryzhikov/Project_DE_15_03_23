import boto3
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# get the input arguments passed in from the Glue job
args = getResolvedOptions(sys.argv, ["JOB_NAME", "s3_bucket"])

# set up the S3 bucket and Glue context
s3_bucket = args["s3_bucket"]
s3_client = boto3.client("s3")
glue_context = GlueContext(SparkContext.getOrCreate())

# create a Glue dynamic frame from the CSV files in the s3 bucket
ticker = "AAPL"
s3_folder_path = f"s3://{s3_bucket}/{ticker}/"
s3_file_path = s3_folder_path + f"{ticker}.csv"
s3_shares_path = s3_folder_path + f"{ticker}_shares.csv"
s3_earnings_path = s3_folder_path + f"{ticker}_earnings.csv"

df = glue_context.create_dynamic_frame_from_options(
    connection_type="s3",
    connection_options={"paths": [s3_file_path], "recurse": True},
    format="csv",
    format_options={"header": True, "inferSchema": True, "delimiter": ","},
).toDF()

# load the shares data and join it with the main data frame
shares_df = spark.read.format("csv").option("header", "true").load(s3_shares_path)
df = df.join(shares_df, on=["Date"])

# group the data by year and calculate the average closing price
df = (
    df.withColumn("year", year("Date"))
    .groupBy("year")
    .agg(avg("Close").alias("average_close"))
)

# write the transformed data to a new S3 bucket
s3_output_path = f"s3://{s3_bucket}/{ticker}_output/"
df.write.mode("overwrite").option("header", "true").csv(s3_output_path)

"""calculating the avg closing price for one stock """
