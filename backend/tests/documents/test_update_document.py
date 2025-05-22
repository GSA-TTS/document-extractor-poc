from unittest import mock

import pytest

from src import context
from src.database.database import Database
from src.database.exception import DatabaseException
from src.documents import update_document

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_update_document_works():
    mock_database = mock.MagicMock()
    context.register(Database, mock_database)

    expected_document_id = "DogCow"
    expected_extracted_data = {
        "name": "Clarus",
    }

    update_document.update_document(expected_document_id, expected_extracted_data)
    mock_database.update_document.assert_called_with(expected_document_id, expected_extracted_data)


def test_update_document_fails():
    mock_database = mock.MagicMock()
    mock_database.update_document.side_effect = DatabaseException("oops")
    context.register(Database, mock_database)

    expected_document_id = "DogCow"
    expected_extracted_data = {
        "name": "Clarus",
    }

    with pytest.raises(DatabaseException):
        update_document.update_document(expected_document_id, expected_extracted_data)
