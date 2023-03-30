import boto3
import argparse


def delete_all_objects_in_bucket(bucket_name):
    """
    Delete all objects in a given S3 bucket
    """
    s3 = boto3.resource("s3", endpoint_url="http://localhost:4566")
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        obj.delete()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete all objects in an S3 bucket")
    parser.add_argument(
        "--bucket", default="bronzelayer", help="S3 bucket name (default: bronzelayer)"
    )
    args = parser.parse_args()

    bucket_name = args.bucket

    # Check if bucket exists
    s3 = boto3.resource("s3", endpoint_url="http://localhost:4566")
    if not any(bucket.name == bucket_name for bucket in s3.buckets.all()):
        print(f"Error: Bucket {bucket_name} does not exist")
    else:
        delete_all_objects_in_bucket(bucket_name)
        print(f"All objects deleted from {bucket_name}")
