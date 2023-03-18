import boto3

# need to change it to IAM role with terraform!!!
#  dont wanna send plain text creds
session = boto3.Session(
    aws_access_key_id="AKIAXBA6QYYMDVI7NFFO",
    aws_secret_access_key="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",
)
sts = session.client("sts")
print(sts.get_caller_identity())
