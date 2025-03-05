# CloudFormation Python Lambda Project

This repository contains a CloudFormation template to deploy an AWS Lambda function, an SQS queue, and an EventBridge rule. The Lambda function is configured to monitor the SQS queue and can be triggered by the EventBridge rule when a new SQS queue is created. The template also includes the necessary IAM roles and permissions to ensure secure and seamless operation.

## Project Structure

```
cloudformation-python-lambda
├── src
│   ├── lambda_function.py
├── templates
│   └── cloudformation-template.yaml
├── README.md
└── requirements.txt
```

## Lambda Function

The Lambda function is located in `src/lambda_function.py`. It performs the following checks on newly created SQS queues:

- Verifies the existence of a VPC endpoint for SQS.
- Ensures encryption-at-rest is enabled.
- Confirms the use of a customer-managed key (CMK).
- Checks for specific tags.

## CloudFormation Template

The CloudFormation template is located in `templates/cloudformation-template.yaml`. It defines the following resources:

- A Python-based Lambda function.
- An IAM role with a permission boundary to restrict actions across accounts.
- An EventBridge rule that triggers the Lambda function on SQS queue creation events.

### Required Parameters

The CloudFormation template requires the following parameters:

- `LambdaRuntime`: The runtime environment for the Lambda function (e.g., `python3.8`).
- `CodeS3Bucket`: S3 bucket where the Lambda function code is stored.

## Deployment Instructions

To deploy the CloudFormation stack, follow these steps:

1. **Package the Lambda function**:
   Ensure that all dependencies listed in `requirements.txt` are installed and the Lambda function is packaged correctly.

2. **Deploy using AWS CLI**:
   Use the following command to deploy the CloudFormation stack:
   ```bash
   aws cloudformation create-stack \
   --stack-name MyStackName \
   --template-body file://template.yaml \
   --parameters ParameterKey=CodeS3Bucket,ParameterValue=your-s3-bucket-name \
                  ParameterKey=CodeS3Key,ParameterValue=your-lambda-code.zip \
                  ParameterKey=LambdaRuntime,ParameterValue=python3.9 \
                  ParameterKey=LambdaMemorySize,ParameterValue=128 \
   --capabilities CAPABILITY_NAMED_IAM
   ```

3. **Verify the deployment**:
   After deployment, check the AWS Management Console for the created resources, including the Lambda function and EventBridge rule.

### Outputs

the template provides the following outputs:

- `SQSQueueUrl`: The URL of the created SQS queue.
- `LambdaFunctionArn` :	The ARN of the deployed Lambda function.
- `LambdaExecutionRoleArn` :	The ARN of the IAM role for the Lambda function.