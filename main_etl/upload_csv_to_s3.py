import os
import boto3

# Set up the S3 client
s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

# Set the directory path to copy files from
dir_path = "data/"

# Set the S3 bucket and prefix to copy files to
s3_bucket = "bronzelayer"
s3_prefix = "data/"

# Recursively walk through the directory tree and copy all CSV files to S3
for subdir, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".csv"):
            # Get the local file path
            local_path = os.path.join(subdir, file)
            # Create the S3 key using the prefix and relative path
            s3_key = os.path.join(s3_prefix, os.path.relpath(local_path, dir_path))
            # Upload the file to S3
            s3.upload_file(local_path, s3_bucket, s3_key)
            print(f"Uploaded {local_path} to s3://{s3_bucket}/{s3_key}")
