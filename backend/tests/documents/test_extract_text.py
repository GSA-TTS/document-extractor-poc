from unittest import mock

import pytest
from types_boto3_sqs import SQSClient

from src import context
from src.documents import extract_text
from src.ocr import Ocr
from src.storage import CloudStorage

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_extract_text_bad_file():
    mock_cloud_storage = mock.MagicMock()
    mock_cloud_storage.file_exists_and_allowed_to_access.return_value = False
    context.register(CloudStorage, mock_cloud_storage)

    with pytest.raises(FileNotFoundError):
        extract_text.extract_text("httpssss://a_sweet/file/location.txt", "https://asdf/queue/url")


def test_extract_text_with_no_form_identified():
    mock_cloud_storage = mock.MagicMock()
    mock_cloud_storage.file_exists_and_allowed_to_access.return_value = True
    context.register(CloudStorage, mock_cloud_storage)

    mock_ocr = mock.MagicMock()
    mock_ocr.extract_raw_text.return_value = ["Don't", "put", "any", "identifying", "words", "here"]
    mock_ocr.scan.return_value = {
        "example key": {
            "value": "example value",
            "confidence": 1.0,
        },
    }
    context.register(Ocr, mock_ocr)

    mock_queue = mock.MagicMock()
    context.register(SQSClient, mock_queue)

    extract_text.extract_text("httpssss://a_sweet/file/location.txt", "https://asdf/queue/url")

    mock_ocr.scan.assert_called_with(mock.ANY, queries=None)
    args, kwargs = mock_queue.send_message.call_args
    assert """"document_type": null""" in kwargs["MessageBody"]
