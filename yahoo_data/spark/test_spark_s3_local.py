# configure spark for S3
hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("fs.s3a.access.key", "mock")
hadoop_conf.set("fs.s3a.secret.key", "mock")
hadoop_conf.set("mapreduce.fileoutputcommitter.algorithm.version", "2")
spark.conf.set("spark.sql.shuffle.partitions", "1")

# configure spark for localstack s3
hadoop_conf.set("fs.s3a.endpoint", "http://127.0.0.1:4572")
hadoop_conf.set("fs.s3a.path.style.access", "true")

# create s3 bucket
import boto3

boto3.resource("s3", endpoint_url="http://127.0.0.1:4572").Bucket(
    "test-bucket"
).create()

# create tiny dataframe and write it to S3 as parquet
df = spark.createDataFrame(
    [
        ("column 1 value 1", "column 2 value 1"),
        ("column 1 value 2", "column 2 value 2"),
        ("column 1 value 3", "column 2 value 3"),
        ("column 1 value 4", "column 2 value 4"),
        ("column 1 value 5", "column 2 value 5"),
        ("column 1 value 6", "column 2 value 6"),
        ("column 1 value 7", "column 2 value 7"),
        ("column 1 value 8", "column 2 value 8"),
    ],
    ["column_1", "column_2"],
)

df.write.parquet("s3://test-bucket/test-parquet/", mode="overwrite")
