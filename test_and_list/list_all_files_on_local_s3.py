import boto3

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

bucket_name = "bronzelayer"

response = s3.list_objects_v2(Bucket=bucket_name)

print(response.keys())
for obj in response["Contents"]:
    print(obj["Key"])
