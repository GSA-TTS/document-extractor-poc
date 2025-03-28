import json

from types_boto3_sqs import SQSClient

from src import context
from src.forms import Form, supported_forms
from src.ocr import Ocr
from src.storage import CloudStorage


@context.inject
def extract_text(remote_file_url: str, queue_url: str, ocr_engine: Ocr = None, sqs_client: SQSClient = None):
    check_that_file_is_good(remote_file_url)

    document_text = ocr_engine.extract_raw_text(remote_file_url)

    identified_form = identify_form(document_text)

    queries = identified_form.queries() if identified_form else None
    extracted_data = ocr_engine.scan(remote_file_url, queries=queries)

    document_type = identified_form.identifier() if identified_form else None
    sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(
            {
                "document_url": remote_file_url,
                "extracted_data": extracted_data,
                "document_type": document_type,
            }
        ),
    )
    print("Message sent to queue successfully")


def identify_form(document_text: list[str]) -> Form:
    identified_form = None

    for text in document_text:
        for form in supported_forms:
            if form.form_matches() in text:
                identified_form = form
                break

    return identified_form


@context.inject
def check_that_file_is_good(remote_file_url: str, cloud_storage: CloudStorage = None):
    good = cloud_storage.file_exists_and_allowed_to_access(remote_file_url)
    if not good:
        raise FileNotFoundError(f"File {remote_file_url} not found")


@context.inject
def send_queue_message_to_next_step(queue_url: str, message: str, sqs_client: SQSClient = None):
    sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
