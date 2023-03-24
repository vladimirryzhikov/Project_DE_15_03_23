import boto3

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

bucket_name = "testbucket"

response = s3.list_objects_v2(Bucket=bucket_name)

for obj in response["Contents"]:
    print(obj["Key"])
