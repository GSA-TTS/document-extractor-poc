import base64
import json
import os
from decimal import Decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.client("dynamodb")
s3_client = boto3.client("s3")

DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")
S3_BUCKET = os.getenv("S3_BUCKET")

deserializer = TypeDeserializer()


def convert_decimal(value):
    """Recursively converts Decimal to float."""
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    elif isinstance(value, list):
        return [convert_decimal(v) for v in value]
    elif isinstance(value, dict):
        return {k: convert_decimal(v) for k, v in value.items()}
    return value


def unmarshal_dynamodb_json(dynamodb_data):
    """Converts DynamoDB JSON format to standard JSON using TypeDeserializer and handles Decimals."""
    deserialized_data = {k: deserializer.deserialize(v) for k, v in dynamodb_data.items()}
    return convert_decimal(deserialized_data)


def lambda_handler(event, context):
    try:
        document_id = event.get("pathParameters", {}).get("document_id")
        if not document_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing document_id in request"}),
            }

        response = dynamodb.get_item(TableName=DYNAMODB_TABLE, Key={"document_id": {"S": document_id}})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Document not found"}),
            }

        item = unmarshal_dynamodb_json(response["Item"])

        document_details = {
            "document_id": item["document_id"],
            "document_key": item["document_key"],
            "document_type": item["document_type"],
            "extracted_data": item.get("extracted_data", {}),
        }

        # Generate signed URL for the document in S3
        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": item["document_key"]},
            ExpiresIn=3600,  # URL expires in 1 hour
        )

        document_details["signed_url"] = signed_url
        # Added this to support UI rendering for demo as there were issue rendering the file via signed url on UI.
        # This need to be looked into from the prespective of whats best for the UI.
        try:
            s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=item["document_key"])
            file_content = s3_object["Body"].read()
            base64_encoded_file = base64.b64encode(file_content).decode("utf-8")
            document_details["base64_encoded_file"] = base64_encoded_file
        except Exception as e:
            return {"error": f"Failed to fetch file: {str(e)}"}

        return {"statusCode": 200, "body": json.dumps(document_details)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
