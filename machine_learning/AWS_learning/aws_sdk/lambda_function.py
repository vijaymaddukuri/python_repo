# Importing Boto3
import boto3
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

iam = boto3.client('lambda',
                   aws_access_key_id="AKIAWZ42OIVQELVZVQQZ",
                   aws_secret_access_key= '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',
                   region_name='ap-south-1')
response = iam.invoke(FunctionName='celebrity_detect_func',
                     InvocationType="RequestResponse",
                     LogType='Tail',
                     Payload = json.dumps({
                         "bucket": "vijay-bucket1986",
                         "object_name": "bezos-image.jpg"
                     }))
celebrity_name = response['Payload'].read().decode('utf8')
print(celebrity_name)