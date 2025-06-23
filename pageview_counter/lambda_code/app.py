import json
import boto3
import logging
from botocore.exceptions import ClientError
import traceback

# Initialize DynamoDB resource and specify the table
dynamodb = boto3.resource("dynamodb")
table_name = "pageview_counter"
table = dynamodb.Table(table_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lambda function to handle pageview counting
def lambda_handler(event, context):
    try:
        logger.info("Lambda triggered with event: %s", json.dumps(event))
        logger.info("Attempting to update DynamoDB table: %s", table_name)
        # Increment the view count atomically in DynamoDB
        response = table.update_item(
            Key={"page": "home"},
            UpdateExpression="ADD #v :incr",
            ExpressionAttributeNames={"#v": "views"},
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="UPDATED_NEW"
        )
        logger.info("DynamoDB update response: %s", response)
        views = int(response["Attributes"]["views"])
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
        logger.error("DynamoDB update failed: %s", str(e))
        logger.error("Traceback: %s", traceback.format_exc())
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": e.response["Error"]["Message"],
                "trace": traceback.format_exc()
            })
        }