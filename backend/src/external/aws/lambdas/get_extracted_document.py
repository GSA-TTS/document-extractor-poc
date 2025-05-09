import base64
import json
import logging

from src import context
from src.database.database import Database
from src.documents import get_document
from src.external.aws.dynamodb import DynamoDb
from src.external.aws.s3 import S3
from src.storage import CloudStorage

appContext = context.ApplicationContext()
appContext.register(CloudStorage, S3())
appContext.register(Database, DynamoDb())


def lambda_handler(event, context):
    document_id = event.get("pathParameters", {}).get("document_id")
    if document_id is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing document_id in path parameter"}),
        }

    try:
        document_info, storage_access_url, document_data = get_document.get_document(document_id)

        if document_info is None:
            return {
                "statusCode": 404,
                "body": json.dumps(f"Document {document_id} not found"),
            }

        response = {
            "status": document_info.status,
            "document_id": document_id,
            "document_key": document_info.document_url,
            "document_type": document_info.document_type,
            "extracted_data": document_info.extracted_data,
            "signed_url": storage_access_url,
            "base64_encoded_file": base64.b64encode(document_data).decode("utf-8"),
        }
    except Exception as e:
        exception_message = f"An internal error happened while trying to get document {document_id}"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    return {"statusCode": 200, "body": json.dumps(response)}
