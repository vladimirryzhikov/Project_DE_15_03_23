import boto3

session = boto3.Session(profile_name="default")

s3 = session.resource("s3")
if not s3.Bucket("bronzelayer") in s3.buckets.all():
    s3.create_bucket(
        Bucket="bronzelayer",
        CreateBucketConfiguration={"LocationConstraint": "eu-north-1"},
    )
result = s3.get_bucket_acl(Bucket="bronzelayer")
print(result)
