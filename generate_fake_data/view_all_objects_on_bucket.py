import boto3

session = boto3.Session(profile_name="default")

s3 = session.resource("s3")
bucket = s3.Bucket("bronzelayer")
for obj in bucket.objects.all():
    print(obj.key)
    