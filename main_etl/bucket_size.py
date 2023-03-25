import boto3

source_bucket_name = "testbucket"
destination_bucket_name = "bronzelayer"

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


# Get bucket size in bytes
bucket_size = 0
response = s3.list_objects_v2(Bucket=source_bucket_name)
for obj in response["Contents"]:
    bucket_size += obj["Size"]

# Convert bytes to MB
bucket_size_mb = bucket_size / 1024 / 1024

print(f"The size of {source_bucket_name} bucket is {bucket_size_mb:.2f} MB")


bucket_size = 0
response = s3.list_objects_v2(Bucket=destination_bucket_name)
for obj in response["Contents"]:
    bucket_size += obj["Size"]

# Convert bytes to MB
bucket_size_mb = bucket_size / 1024 / 1024

print(f"The size of {destination_bucket_name} bucket is {bucket_size_mb:.2f} MB")
