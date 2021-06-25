# Importing Boto3
import boto3

# Creating S3 client
s3 = boto3.client('s3', aws_access_key_id="AKIAWZ42OIVQELVZVQQZ",aws_secret_access_key= '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')

# Listing the buckets
response = s3.list_buckets()

# Printing the response variable
print(response)

# Printing the bucket names
for bucket in response['Buckets']:
    print(bucket['Name'])