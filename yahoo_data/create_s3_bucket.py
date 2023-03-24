import boto3

# Create an S3 client on localstack
s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

# Set the bucket name
bucket_name = "testbucket"

# Set the region (replace with your desired region)
region = "eu-north-1"

# Create the bucket with the specified region
response = s3.create_bucket(
    Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region}
)

# Print the response
print(response)
