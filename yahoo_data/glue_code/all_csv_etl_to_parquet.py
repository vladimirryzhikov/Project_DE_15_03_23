import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

# Initialize a Spark context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Get the S3 source and destination paths from the job parameters
args = getResolvedOptions(sys.argv, ["source_bucket", "destination_bucket"])
source_bucket = args["source_bucket"]
destination_bucket = args["destination_bucket"]

# Read the CSV files from the source S3 bucket and create a dynamic frame
df = (
    spark.read.format("csv")
    .option("header", "true")
    .load(f"s3://{source_bucket}/*/*.csv")
)
df.printSchema()

# Transformations
df = df.filter(
    col("Close") > 50
)  # Keep only records where the closing price is over 50
df = df.withColumn(
    "Daily_Return", ((col("Close") - col("Open")) / col("Open")) * 100
)  # Calculate daily return percentage

# Write the transformed data to a new S3 bucket
output_path = f"s3://{destination_bucket}/output"
df.write.mode("overwrite").parquet(output_path)


""" we're reading in all CSV files from the source S3 bucket,
 filtering records based on a condition, 
 and calculating a new column based on existing columns. 
 Finally, we're writing the results to a new S3 bucket in Parquet 
 format. Note that you'll need to replace the source_bucket 
 and destination_bucket parameters with the actual bucket names 
 that you're using """
