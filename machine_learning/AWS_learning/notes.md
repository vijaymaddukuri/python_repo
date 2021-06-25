## Create user:

aws iam create-user --user-name vijaym

## command to assign the user ‘user1’ the following permission: AdministratorAccess?
aws iam attach-user-policy --user-name vijaym --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Creating a group
aws iam create-group --group-name group1

# Adding user to the group
aws iam add-user-to-group --user-name vijaym --group-name group1

# Fetching the group details
aws iam get-group --group-name group1

# Opening the json file that stores the policy to allow S3 access
vi test.json

# Creating a policy using the json file
aws iam create-policy --policy-name policy1 --policy-document file:///Users/vmaddukuri/python_repo/machine_learning/AWS_learning/test.json

# Make sure that you copy the policy ARN here as it will be used later

# Opening the json file that stores the role that allows EC2 to assume the Role
vi test_role.json

# Creating a role using the json file
aws iam create-role --role-name role1 --assume-role-policy-document file:///Users/vmaddukuri/python_repo/machine_learning/AWS_learning/test_role.json

# Attaching the policy to the created role
aws iam attach-role-policy --role role1 --policy-arn "arn:aws:iam::467938461024:policy/policy1"

# Checking the created role
aws iam list-attached-role-policies --role-name role1

#How can I find the resources associated with an Amazon EC2 security group?
##Run the following command in the AWS CLI to find network interfaces associated with a security group based on the security group ID.

aws ec2 describe-network-interfaces --filters Name=group-id,Values=<group-id> --region <region> --output json

## If the output contains results, you can find more information about the resources associated with the security group using the following command.

aws ec2 describe-network-interfaces --filters Name=group-id,Values=<group-id> --region <region> --output json --query 'NetworkInterfaces[*]'.['NetworkInterfaceId','Description','PrivateIpAddress','VpcId']

# How does Amazon identify the resources that are available on the AWS Cloud network?
AWS tracks all the resources on its platform through Amazon Resource Names, or ARNs. 
ARNs help with uniquely identifying all the resources across all the users and services available on the 
platform through their unique structure, arn:partition:service:region:account-id:resource-type/resource-id

# AWS CLI: S3

## S3 Commands
## Creating a bucket - mb command

aws s3 mb s3://vijay-bucket1986
## Listing the buckets in S3 - ls command
aws s3 ls

## Copying a file from local machine to S3 bucket - cp command
aws s3 cp ./test.json s3://vijay-bucket1986/file_name.json

## Listing the objects in the bucket - ls command
aws s3 ls s3://vijay-bucket1986

## Removing a file from the bucket - rm command
aws s3 rm s3://vijay-bucket1986/file_name.json

## Removing all the files from the bucket - rm command
aws s3 rm --recursive s3://vijay-bucket1986

## Removing the bucket - rb command
aws s3 rb s3://vijay-bucket1986

## How will you delete a bucket that contains multiple files and folders?
aws s3 rb --force s3://bucket_name

## Move objects
aws s3 mv <source> <target> [--options]

## Copy objects
aws s3 cp <source> <target> [--options]
ex: aws s3 cp s3://bucket-name/example s3://my-bucket/

### Suppose you work in an e-commerce company that keeps records of multiple products (more than a thousand) in the S3 bucket ‘records’. The files have the following structure for filename: ‘category-productid.csv’.

### You have to analyse the records associated with the ‘Electronics’ category only. You are expected to download specific category reports and then perform analysis over your local machine.

### Provide the command that helps you perform this task.
aws s3 cp s3://records “local_path” --recursive --exclude “*” --include “electronics*”


# EC2 Commands
## Creating a VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

## VPC Details
aws ec2 describe-vpcs --vpc-ids vpc_ID_from_above_command

## Creating subnet 1
aws ec2 create-subnet --vpc-id vpc_ID_from_above_command --cidr-block 10.0.1.0/24

## Copy the subnet ID for subnet 1 from here

## Creating subnet 2
aws ec2 create-subnet --vpc-id vpc_ID_from_above_command --cidr-block 10.0.2.0/24

## Copy the subnet ID for subnet 2 from here

## Subnet 1 Details
aws ec2 describe-subnets --subnet-ids subnet_1_ID_copied_from_above

## Creating internet gateway
aws ec2 create-internet-gateway

## Copy the Internet Gateway ID from here

## Attaching the internet gateway with the VPC created before
aws ec2 attach-internet-gateway --vpc-id vpc_ID --internet-gateway-id internet_gateway_ID

## Create Route table
aws ec2 create-route-table --vpc-id vpc_ID

## Copy the Route table ID from here

## Attaching the route table to the internet gateway
aws ec2 create-route --route-table-id route_table_ID --destination-cidr-block 0.0.0.0/0 --gateway-id internet_gateway_ID

## Attaching the route table with the subnet 1
aws ec2 associate-route-table --subnet-id subnet_1_ID --route-table-id route_table_ID

## Code to map a public IP to the instance on launch
aws ec2 modify-subnet-attribute --subnet-id subnet_1_ID --map-public-ip-on-launch

## Creating key pair
aws ec2 create-key-pair --key-name keypair1 --output text --query "KeyMaterial"> keypair1.pem

## Opening the .pem file (Windows)
## Open using the 'Notepad' application

## Opening the .pem file (Linux/Mac)
vi keypair1.pem

## Changing the permission to read only (Linux/Mac)
chmod 400 keypair1.pem

## Creating Security Group
aws ec2 create-security-group --group-name test_group --description "Security group for demo" --vpc-id vpc_ID

## Copy Security Group ID as it will be helpful later

## Adding rule to your security group to permit access from your laptop - Ports 22 and 8888
aws ec2 authorize-security-group-ingress --group-id security_group_id_from_above --protocol tcp --port 22 --cidr your_public_ip
aws ec2 authorize-security-group-ingress --group-id security_group_id_from_above --protocol tcp --port 8888 --cidr your_public_ip

## Initiating an ec2 instance
aws ec2 run-instances --image-id correct_AMI_ID_from_document --count 1 --instance-type t2.micro --key-name keypair1 --security-group-ids security_group_id_from_above --subnet-id subnet_1_ID

## Copy ths instance ID from above

## Describing the details of the instance
aws ec2 describe-instances --instance-id Instance_ID_from_above

## Logging into the instance in a LINUX/Mac environment
ssh -i keypair1.pem ec2-user@EC2_instance_public_IP

## Starting an existing instance
aws ec2 start-instances --instance-ids Instance_ID

## Creating an instance profile to attach the role to the instance
aws iam create-instance-profile --instance-profile-name instanceprofile1

## Attaching the created role to the instance profile
aws iam add-role-to-instance-profile --role-name role1 --instance-profile-name instanceprofile1

## Attaching the instance profile to the instance
aws ec2 associate-iam-instance-profile --instance-id Instance_ID --iam-instance-profile Name=instanceprofile1

## Stopping the instance
aws ec2 stop-instances --instance-ids Instance_ID

##Decode message
aws sts decode-authorization-message --encoded-message 

# Configure default region
aws configure set default.region us-east-1

# Amazon Comprehend
Amazon Comprehend is a text analytics service that finds insights and relationships in a text. 
It uses the Natural Language Processing (NLP) function in the background to accomplish the task.

# Amazon Transcribe
which is a speech-to-text service that transcribes audio in real time. 

#Amazon Polly
used to generate audio from text files. 

# Amazon Translate 
Translates text from one language to another. 
The service is highly accurate and evolves with every job that is run on it.
It supports 54 different languages that are listed on the service page. 
The key advantage of using this service is that entities such as popular 
brand names and industry terms are kept intact in the translated text. 
You can even define custom terminologies to do the same for items specific to your job.

# Amazon Rekognition
Amazon Rekognition is a powerful tool that can be used to perform visual (image and video) analysis in your applications. 

# Amazon CloudWatch
A monitoring service offered by AWS
Amazon CloudWatch is a unified platform on which you can monitor all the AWS resources, 
applications and services through associated logs, metrics and events. 
It serves as a useful tool for DevOps engineers, developers, 
site reliability engineers (SREs) and IT managers since all the resources can be monitored under a single service.

Amazon CloudWatch collects all the data and helps with visualising it in the form of automated dashboards. 
These dashboards help with tracking the usage and health of each resource in the Cloud infrastructure. 
You can easily find areas of improvement or possible failures by keeping an eye on the desired metrics 
for each service. This leads to better management and optimisation of processes and costs. 
Take a look at the image given below to understand the working of CloudWatch.

# Software Development Kits (SDKs)
Helps you build or develop applications for specific hardware or software platforms. 







