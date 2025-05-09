from unittest import mock

import pytest

from src import context
from src.database.data.document_item import DocumentItem
from src.database.database import Database
from src.database.exception import DatabaseException
from src.documents import get_document
from src.storage import CloudStorage, CloudStorageException

context = context.ApplicationContext()


def setup_function():
    context.reset()


def test_get_document_no_document_exists():
    """get_document returns None if document does not exist in the database."""
    mock_database = mock.MagicMock()
    mock_database.get_document.return_value = None
    context.register(Database, mock_database)

    document_info, storage_access_url, document_data = get_document.get_document("document ID of wonder")

    assert document_info is None
    assert storage_access_url is None
    assert document_data is None


def test_get_document_database_raise_exception():
    """get_document continues to raise an exception if the database raises an exception."""
    mock_database = mock.MagicMock()
    exception = DatabaseException("something went wrong")
    mock_database.get_document.side_effect = exception
    context.register(Database, mock_database)

    with pytest.raises(DatabaseException):
        get_document.get_document("document ID of wonder")


def test_get_document_cloud_storage_access_url_raise_exception():
    """get_document continues to raise an exception if the cloud storage raises an exception."""

    mock_database = mock.MagicMock()
    mock_database.get_document.return_value = {"document_url": "DogCow goes Moof!"}
    context.register(Database, mock_database)

    mock_cloud_storage = mock.MagicMock()
    exception = CloudStorageException("something went wrong")
    mock_cloud_storage.access_url.side_effect = exception
    context.register(CloudStorage, mock_cloud_storage)

    with pytest.raises(CloudStorageException):
        get_document.get_document("document ID of wonder")


def test_get_document_cloud_storage_get_document_raise_exception():
    """get_document continues to raise an exception if the cloud storage raises an exception."""

    mock_database = mock.MagicMock()
    mock_database.get_document.return_value = {"document_url": "DogCow goes Moof!"}
    context.register(Database, mock_database)

    mock_cloud_storage = mock.MagicMock()
    exception = CloudStorageException("something went wrong")
    mock_cloud_storage.get_file.side_effect = exception
    context.register(CloudStorage, mock_cloud_storage)

    with pytest.raises(CloudStorageException):
        get_document.get_document("document ID of wonder")


def test_get_document_works():
    """The whole flow works and returns expected data."""

    mock_database = mock.MagicMock()
    document_id = "document ID of wonder"
    document_url = "The direct URL of the document"
    expected_document_info = DocumentItem(document_id, document_url)
    mocked_document_info = {"document_id": document_id, "document_url": document_url}
    mock_database.get_document.return_value = mocked_document_info
    context.register(Database, mock_database)

    mock_cloud_storage = mock.MagicMock()
    expected_access_url = "A different URL"
    expected_document_data = b"DogCow goes Moof!"
    mock_cloud_storage.access_url.return_value = expected_access_url
    mock_cloud_storage.get_file.return_value = expected_document_data
    context.register(CloudStorage, mock_cloud_storage)

    document_info, storage_access_url, document_data = get_document.get_document(expected_document_info.document_id)

    assert document_info == expected_document_info
    assert storage_access_url == expected_access_url
    assert document_data == expected_document_data
