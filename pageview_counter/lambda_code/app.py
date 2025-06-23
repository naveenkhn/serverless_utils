import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource and specify the table
dynamodb = boto3.resource("dynamodb")
table_name = "pageview_counter"
table = dynamodb.Table(table_name)

# Lambda function to handle pageview counting
def lambda_handler(event, context):
    try:
        # Increment the view count atomically in DynamoDB
        response = table.update_item(
            Key={"page": "home"},
            UpdateExpression="ADD views :incr",
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="UPDATED_NEW"
        )
        views = response["Attributes"]["views"]
        # Return the updated view count in the response
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"views": views})
        }

    except ClientError as e:
        # Handle any DynamoDB client errors and return error message
        return {
            "statusCode": 500,
            "body": json.dumps({"error": e.response["Error"]["Message"]})
        }