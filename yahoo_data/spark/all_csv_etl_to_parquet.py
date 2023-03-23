import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# from moto import mock_s3, mock_sts
import boto3


# NEED TO BE TESTED WHEN GLUE AVALAIBILITY IS DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Initialize a Spark context
# spark = SparkSession.builder.appName("local-spark-job").getOrCreate()
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

""" spark._jsc.hadoopConfiguration().set(
    "fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
)
 """
# Get the S3 source and destination buckets
source_bucket = "bronzelayer"
destination_bucket = "silverlayer"

# Read the CSV files from the source S3 bucket and create a dynamic frame
df = (
    spark.read.format("csv")
    .option("header", "true")
    .load(f"s3a://{source_bucket}/*/*.csv")
)
df.printSchema()

# Transformations
df = df.filter(
    col("Close") > 50
)  # Keep only records where the closing price is over 50
df = df.withColumn(
    "Daily_Return", ((col("Close") - col("Open")) / col("Open")) * 100
)  # Calculate daily return percentage
df.show()  # show the results
# Write the transformed data to a new S3 bucket
output_path = f"s3a://{destination_bucket}/output"
df.write.mode("overwrite").parquet(output_path)


""" we're reading in all CSV files from the source S3 bucket,
 filtering records based on a condition, 
 and calculating a new column based on existing columns. 
 Finally, we're writing the results to a new S3 bucket in Parquet 
 format. Note that you'll need to replace the source_bucket 
 and destination_bucket parameters with the actual bucket names 
 that you're using """
