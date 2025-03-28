import json
import os
from decimal import Decimal

import boto3

dynamodb = boto3.resource("dynamodb")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")


def convert_to_dynamodb_format(data):
    """Ensures all float values are converted to decimal for DynamoDB storage."""

    def replace_floats(obj):
        """Recursively convert all float values to decimal to ensure DynamoDB compatibility."""
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: replace_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_floats(i) for i in obj]
        else:
            return obj

    return replace_floats(data)


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"), parse_float=Decimal)
        document_id = event.get("pathParameters", {}).get("document_id")
        new_extracted_data = body.get("extracted_data")

        if not document_id or new_extracted_data is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing document_id or extracted_data in request"}),
            }

        cleaned_data = convert_to_dynamodb_format(new_extracted_data)

        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression="SET extracted_data = :new_data",
            ExpressionAttributeValues={":new_data": cleaned_data},
            ReturnValues="ALL_NEW",
        )

        print(f"Update Response: {response}")

        updated_item = response.get("Attributes", {})

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Document updated successfully",
                    "updated_document": updated_item,
                },
                default=str,
            ),
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
