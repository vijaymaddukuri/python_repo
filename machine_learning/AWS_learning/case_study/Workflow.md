# Creating a role ​csdrole​ ​with the role policy document:
aws iam create-role --role-name csdrole --assume-role-policy-document file:///Users/vmaddukuri/python_repo/machine_learning/AWS_learning/test_role.json

Output: 
"RoleName": "csdrole",
"RoleId": "AROAWZ42OIVQHSA55LKII",
"Arn": "arn:aws:iam::467938461024:role/csdrole"

# Attaching the S3 and Lambda full access policies to the created role
aws iam attach-role-policy --role-name csdrole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name csdrole --policy-arn arn:aws:iam::aws:policy/AWSLambdaFullAccess

# An instance profile is used to attach a role to the EC2 instance. To create an instance profile,
aws iam create-instance-profile --instance-profile-name csdinstanceprofile

{
"InstanceProfile": {
"Path": "/",
"InstanceProfileName": "csdinstanceprofile",
"InstanceProfileId": "AIPAWZ42OIVQAGTIBQHLW",
"Arn": "arn:aws:iam::467938461024:instance-profile/csdinstanceprofile",
"CreateDate": "2021-05-08T14:40:32Z",
"Roles": []
}
}

# Adding role ​csdrole ​to the instance profile ​csdinstanceprofile ​(created above)
aws iam add-role-to-instance-profile --role-name csdrole --instance-profile-name csdinstanceprofile

# Creating the Security group and Access key pair
aws ec2 create-security-group --group-name csdjupyteraccess --description "Access for jupyter and ssh"
{
"GroupId": "sg-0ef983fa627c0b5e6"
}

# Authorizing the access of ports 22 and 8888 through local IP address for SSH and Jupyter respectively
aws ec2 authorize-security-group-ingress --group-id sg-0ef983fa627c0b5e6 --protocol tcp --port 22 --cidr 3.95.195.58/32
aws ec2 authorize-security-group-ingress --group-id sg-0ef983fa627c0b5e6 --protocol tcp --port 8888 --cidr 3.95.195.58/32

# Creating an Access key pair for the account (Skip this step if you have a previously created key pair as only 2 keys are allowed per account.)
aws ec2 create-key-pair --key-name csd_pair --query "KeyMaterial" --output text > csd_pair.pem

# Creating the EC2 instance with the above resources
## Now you are going to create an EC2 instance with the resources - 
## Role, Security group and Keypair. You will be using Amazon Linux OS on a t2.micro instance.
aws ec2 run-instances --image-id ami-0d5eff06f840b45e9 --count 1 --instance-type t2.micro --key-name csd_pair --security-group-ids sg-0ef983fa627c0b5e6 --iam-instance-profile Name=csdinstanceprofile

Output: "InstanceId": "i-02d8bb3240cc0975c", "PublicDnsName": "ec2-52-87-184-173.compute-1.amazonaws.com",
"PublicIpAddress": "52.87.184.173"


## can describe the instance using
aws ec2 describe-instances --instance-id i-02d8bb3240cc0975c

## Login into the instance
ssh -i "csd_pair.pem" ec2-user@ec2-52-87-184-173.compute-1.amazonaws.com

#Creating the RDS instance
## Creating a MySQL database named ​celebrities​ through CLI. Do not use the web console as the steps may result 
##in some differences than the process followed.
aws rds create-db-instance --engine mysql --db-name celebrities --db-instance-class db.t2.micro --allocated-storage 20 --db-instance-identifier test-instance --master-username master --master-user-password vijaynov18
aws rds create-db-instance --engine mysql --db-name stackoverflow --db-instance-class db.t2.micro --allocated-storage 20 --db-instance-identifier stackoverflow-instance --master-username master --master-user-password vijaynov18

## Describe command
aws rds describe-db-instances

"Endpoint": {
"Address": "test-instance.ctiigg0x7fppy.us-east-1.rds.amazonaws.com",
"Port": 3306,
"HostedZoneId": "Z2R2ITUGPM61AM"
"VpcSecurityGroupId": "sg-15bb0f10",
},

## Authorising the EC2 and RDS connection by adding EC2 instance IP to the RDS Security group as we will be accessing the SQL database from EC2 instance.

aws ec2 authorize-security-group-ingress --group-id sg-15bb0f10 --protocol tcp --port 3306 --cidr  172.31.21.159/32


Create policy file:
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Principal": {
"Service": "lambda.amazonaws.com"
},
"Action": "sts:AssumeRole"
}
]
}

# Command to create an execution role with the AWS CLI
aws iam create-role --role-name csdlambdarole --assume-role-policy-document file:///Users/vmaddukuri/python_repo/machine_learning/AWS_learning/lambda_policy.json

"RoleId": "AROAWZ42OIVQCJZDGFFXX",
"Arn": "arn:aws:iam::467938461024:role/csdlambdarole",


# Commannd to add permissions to the role, use the attach-policy-to-role command. Start by adding the AWSLambdaBasicExecutionRole managed policy.

aws iam attach-role-policy --role-name csdlambdarole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name csdlambdarole --policy-arn arn:aws:iam::aws:policy/AmazonRekognitionFullAccess
aws iam attach-role-policy --role-name csdlambdarole --policy-arn arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole

# Login to instance
ssh -i /Users/vmaddukuri/Downloads/vijay_keypair.pem -N -f -L 8888:localhost:8888 ec2-user@54.227.61.166

# Install juptyer
pip3 install jupyter --user
jupyter notebook list
# start the Jupyter Notebook server using the command provided below:
jupyter notebook

Now, the Jupyter Notebook is running on the EC2 instance. However, you need to access it
through a browser using SSH tunneling. This step differs for Windows and Linux/Mac
users.

# CONNECTING TO A JUPYTER NOTEBOOK - LINUX/MAC
ssh -i “keypair1.pem” -N -f -L 8888:localhost:8888 ec2-user@IPv4_address_of_EC2 instance

# Open jupyter notebook and creatr sctipt to upload image to se
refer: upload_image.py in aws_sdk

# Create zip file with boto3 installations
create lambda folder
!pip3 install --target ./lambda/boto3 boto3
%cd lambda
!zip -r9 ../celebrity_detector.zip .

# Create handler for rekognition object and upload image
Refer: handler.py in aws_sdk

# Create lambda function
%cd /home/ec2-user
!ls
!export AWS_ACCESS_KEY_ID=AKIAWZ42OIVQELVZVQQZ
!export AWS_SECRET_ACCESS_KEY=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
!aws lambda create-function --function-name celebrity_detect_func --runtime python3.7 --zip-file fileb://celebrity_detector.zip --handler handler.lambda_handler --role arn:aws:iam::467938461024:role/csdlambdarole --region ap-south-1