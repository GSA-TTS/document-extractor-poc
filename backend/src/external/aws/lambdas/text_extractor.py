import json
import logging
import os

import boto3
from aws_lambda_typing import context as lambda_context
from aws_lambda_typing import events
from types_boto3_sqs import SQSClient

from src import context
from src.documents import extract_text
from src.external.aws.s3 import S3
from src.external.aws.textract import Textract
from src.ocr import Ocr, OcrException
from src.storage import CloudStorage

appContext = context.ApplicationContext()
appContext.register(Ocr, Textract())
appContext.register(CloudStorage, S3())
appContext.register(SQSClient, boto3.client("sqs"))

sqs_queue_url = os.environ["SQS_QUEUE_URL"]


def lambda_handler(event: events.S3Event, context: lambda_context.Context):
    record = event["Records"][0]
    bucket_name = record["s3"]["bucket"]["name"]
    document_key = record["s3"]["object"]["key"]

    s3_url = f"s3://{bucket_name}/{document_key}"
    logging.info(f"Processing {s3_url}")

    try:
        extract_text.extract_text(s3_url, sqs_queue_url)
    except FileNotFoundError as e:
        exception_message = f"Failed to find the file {s3_url}"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }
    except OcrException as e:
        exception_message = f"Failed OCR of {s3_url}"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }
    except Exception as e:
        exception_message = "Failed to send message to queue"
        logging.error(exception_message)
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps(exception_message),
        }

    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully and sent to SQS"),
    }
