import json
import boto3
import logging
from botocore.exceptions import ClientError

# Initialize DynamoDB resource and specify the table
dynamodb = boto3.resource("dynamodb")
table_name = "pageview_counter"
table = dynamodb.Table(table_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lambda function to handle pageview counting
def lambda_handler(event, context):
    try:
        # Increment the view count atomically in DynamoDB
        response = table.update_item(
            Key={"page": "home"},
            UpdateExpression="ADD #v :incr",
            ExpressionAttributeNames={"#v": "views"},
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="UPDATED_NEW"
        )
        views = response["Attributes"]["views"]
        # Return the updated view count in the response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"views": views})
        }

    except ClientError as e:
        logger.error("DynamoDB update failed", exc_info=True)
        # Handle any DynamoDB client errors and return error message
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": e.response["Error"]["Message"]})
        }