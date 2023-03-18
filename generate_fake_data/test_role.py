import boto3

session = boto3.Session(profile_name="test")
sts = session.client("sts")
""" response = sts.assume_role(
    RoleArn="arn:aws:iam::xxx:role/s3-readonly-access",
    RoleSessionName="learnaws-test-session",
) """

response = sts.get_caller_identity()
print(response)
