import boto3

# Create an S3 client on localstack
s3 = boto3.client("s3", endpoint_url="http://localhost:4566")

# Set the bucket name
bucket_names = ["testbucket", "bronzelayer", "silverlayer", "goldlayer"]

# Set the region (replace with your desired region)
region = "eu-north-1"

for bucket in bucket_names:
    # Create the bucket with the specified region
    response = s3.create_bucket(
        Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region}
    )
    print(response)
# Print the response
