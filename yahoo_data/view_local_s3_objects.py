import boto3

s3 = boto3.resource("s3", endpoint_url="http://localhost:4566")

bucket_name = "bronzelayer"

# List all objects in the bucket
bucket = s3.Bucket(bucket_name)
for obj in bucket.objects.all():
    print(obj.key)

# View the contents of an object
obj = s3.Object(bucket_name, "path/to/object")
contents = obj.get()["Body"].read().decode("utf-8")
print(contents)
