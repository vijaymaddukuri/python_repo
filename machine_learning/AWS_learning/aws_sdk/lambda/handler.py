# Importing Boto3
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('rekognition',
                          aws_access_key_id="AKIAWZ42OIVQELVZVQQZ",
                          aws_secret_access_key='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')
    response = client.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': event['bucket'],
                'Name': event['object_name']
            }
        }
    )
    return (response['CelebrityFaces'][0]['Name'])
