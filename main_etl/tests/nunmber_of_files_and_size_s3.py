import boto3

bucket_name = "bronzelayer"

s3 = boto3.resource("s3", endpoint_url="http://localhost:4566")
bucket = s3.Bucket(bucket_name)

total_size = 0
total_files = 0

for obj in bucket.objects.all():
    total_size += obj.size
    total_files += 1

print(f"Bucket size: {total_size / (1024*1024):.2f} MB")
print(f"Number of files: {total_files}")
