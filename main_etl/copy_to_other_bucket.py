import boto3

source_bucket_name = "testbucket"
destination_bucket_name = "bronzelayer"

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

# Get a list of all objects in the source bucket
objects = s3.list_objects_v2(Bucket=source_bucket_name)["Contents"]

# Copy each object to the destination bucket
for obj in objects:
    key = obj["Key"]
    s3.copy_object(
        Bucket=destination_bucket_name,
        CopySource={"Bucket": source_bucket_name, "Key": key},
        Key=key,
    )
