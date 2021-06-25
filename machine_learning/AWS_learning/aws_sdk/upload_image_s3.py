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

# Upload image to s3
file_name = 'bezos-image.jpg'
bucket = 'vijay-bucket1986'
object_name = 'bezos-image.jpg'

# s3.upload_file(file_name, bucket, object_name)
response = s3.list_objects(Bucket=bucket)
for objects in response['Contents']:
    print(objects['Key'], objects['Size'])

# !pip3 install --target ./lambda/boto3 boto3
# %cd lambda
#!zip -r9 ../celebrity_detector.zip .
