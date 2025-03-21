import json
import os

import boto3

from src.external.ocr.textract import Textract
from src.forms import supported_forms
from src.ocr import OcrException

s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs")

SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket_name = record["s3"]["bucket"]["name"]
    document_key = record["s3"]["object"]["key"]

    print(f"Processing file: s3://{bucket_name}/{document_key}")

    try:
        metadata = s3_client.head_object(Bucket=bucket_name, Key=document_key)
        print("S3 Metadata Retrieved Successfully:")
        print(metadata)

    except Exception as e:
        print(f"Failed to retrieve S3 object metadata: {e}")
        return {
            "statusCode": 403,
            "body": json.dumps(
                "Failed to access S3 object. Check permissions or other issues with file or configurations."
            ),
        }

    ocr_engine = Textract()

    try:
        document_text = ocr_engine.extract_raw_text(f"s3://{bucket_name}/{document_key}")
    except OcrException as e:
        exception_message = f"Failed to detect the document type of s3://{bucket_name}/{document_key}: {e}"
        print(exception_message)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    identified_form = None

    for text in document_text:
        for form in supported_forms:
            if form.form_matches() in text:
                identified_form = form
                break

    try:
        extracted_data = ocr_engine.scan(f"s3://{bucket_name}/{document_key}", queries=identified_form.queries())
    except OcrException as e:
        exception_message = f"Failed to extract text from S3 object s3://{bucket_name}/{document_key}: {e}"
        print(exception_message)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    # Send extracted data to SQS
    try:
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(
                {
                    "document_key": document_key,
                    "extracted_data": extracted_data,
                    "document_type": identified_form.identifier(),
                }
            ),
        )
        print("Message sent to SQS successfully.")
    except Exception as sqs_error:
        print(f"Failed to send message to SQS: {sqs_error}")

    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully and sent to SQS"),
    }
