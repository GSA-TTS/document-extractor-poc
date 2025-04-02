from unittest import mock

import pytest

from src import context
from src.database.database import Database
from src.database.exception import DatabaseException
from src.documents import write_document

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_write_document_works():
    mock_database = mock.MagicMock()
    context.register(Database, mock_database)

    expected_document_id = "DogCow"
    expected_document_url = f"s3://bucket/moof/{expected_document_id}.txt"
    expected_document_type = "W2"
    expected_extracted_data = {
        "name": "Clarus",
    }
    expected_item = {
        "document_id": expected_document_id,
        "document_url": expected_document_url,
        "document_type": expected_document_type,
        "extracted_data": expected_extracted_data,
    }

    write_document.write_document(expected_document_url, expected_document_type, expected_extracted_data)

    mock_database.write_document.assert_called_with(expected_item)


def test_write_document_fails():
    """write_document fails writing to the database and bubbles up the exception"""
    mock_database = mock.MagicMock()
    mock_database.write_document.side_effect = DatabaseException("oops")
    context.register(Database, mock_database)

    with pytest.raises(DatabaseException):
        write_document.write_document("s3://bucket/moof/DogCow.txt", "W2", {"name": "Clarus"})
