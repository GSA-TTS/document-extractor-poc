import json
import logging
from decimal import Decimal

from src.context import ApplicationContext
from src.database.database import Database
from src.documents import update_document
from src.external.aws.dynamodb import DynamoDb
from src.logging_config import setup_logger

appContext = ApplicationContext()
appContext.register(Database, DynamoDb())

setup_logger()


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

        updated_document_item = update_document.update_document(document_id, new_extracted_data)

        response = {
            "message": "Document updated successfully",
            "status": updated_document_item.status,
            "document_id": document_id,
            "document_key": updated_document_item.document_url,
            "document_type": updated_document_item.document_type,
            "extracted_data": updated_document_item.extracted_data,
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response),
        }

    except Exception as e:
        logging.exception({str(e)})
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
