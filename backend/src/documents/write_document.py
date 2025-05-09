import os
from urllib import parse

from src import context
from src.database.data.document_item import DocumentItem, document_item_to_dict
from src.database.database import Database


@context.inject
def write_document(document_id: str, document_url: str, database: Database = None):
    document_item = DocumentItem(document_id, document_url)
    database.write_document(document_item_to_dict(document_item))


@context.inject
def update_document(document_url: str, document_type: str | None, extracted_data: dict, database: Database = None):
    document_id = convert_document_url_to_id(document_url)
    document_item = DocumentItem(document_id, document_url, "complete", document_type, extracted_data)
    database.write_document(document_item_to_dict(document_item))


def convert_document_url_to_id(document_url: str):
    parsed_url = parse.urlparse(document_url)
    document_key = parsed_url.path
    base = os.path.basename(document_key)
    return os.path.splitext(base)[0]
