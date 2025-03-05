import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs_client = boto3.client('sqs')
ec2_client = boto3.client('ec2')

# Get the SQS queue URL or name from an environment variable
SQS_QUEUE_URL_OR_NAME = os.getenv('SQS_QUEUE_URL_OR_NAME', None)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    # Determine the queue URL or name
    if SQS_QUEUE_URL_OR_NAME:
        logger.info(f"Using SQS queue URL or name from environment variable: {SQS_QUEUE_URL_OR_NAME}")
        queue_url = resolve_queue_url(SQS_QUEUE_URL_OR_NAME)
    else:
        logger.info("Extracting SQS queue URL from the event.")
        queue_url = event['detail']['responseElements']['queueUrl']
    
    queue_name = queue_url.split('/')[-1]
    
    # Check VPC Endpoint
    vpc_endpoints = ec2_client.describe_vpc_endpoints(Filters=[{'Name': 'service-name', 'Values': ['com.amazonaws.us-east-1.sqs']}])
    if not vpc_endpoints['VpcEndpoints']:
        alert(f"No VPC endpoint found for SQS in us-east-1 for queue {queue_name}")
    
    # Ensure that the SQS queue has encryption enabled
    attributes = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])
    if 'KmsMasterKeyId' not in attributes['Attributes']:
        alert(f"Queue {queue_name} does not have encryption enabled.")
    elif not attributes['Attributes']['KmsMasterKeyId'].startswith('arn:aws:kms'):
        alert(f"Queue {queue_name} is not using a customer-managed key (CMK).")
    
    # Check Tags
    tags = sqs_client.list_queue_tags(QueueUrl=queue_url).get('Tags', {})
    required_tags = ['Name', 'Created By', 'Environment']
    for tag in required_tags:
        if tag not in tags:
            alert(f"Queue {queue_name} is missing required tag: {tag}")

def alert(message):
    """
    Logs an error message and optionally sends an alert.
    """
    logger.error(message)
    # Add SNS or other alerting mechanisms here if needed