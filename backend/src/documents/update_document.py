from src import context
from src.database.data.document_item import DocumentItem
from src.database.database import Database


@context.inject
def update_document(document_id: str, document_data: dict, database: Database = None) -> DocumentItem:
    return database.update_document(document_id, document_data)
