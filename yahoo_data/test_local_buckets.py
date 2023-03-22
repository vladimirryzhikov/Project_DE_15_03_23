import boto3


# Create an S3 client
# s3 = boto3.client("s3")
s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

# Call the list_buckets method to get all buckets
response = s3.list_buckets()

# Print each bucket name
print("All S3 Buckets:")
for bucket in response["Buckets"]:
    print(bucket["Name"])
