import os
from decimal import Decimal
from typing import Any

import boto3
from boto3.dynamodb.types import TypeDeserializer
from types_boto3_dynamodb import DynamoDBClient

from src.database.database import Database
from src.database.exception import DatabaseException


class DynamoDb(Database):
    def __init__(self) -> None:
        self.dynamodb_client: DynamoDBClient = boto3.client("dynamodb")
        self.table_name = os.getenv("DYNAMODB_TABLE")
        self.table = self.dynamodb_client.Table(self.table_name)
        self.deserializer = TypeDeserializer()

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        try:
            dynamodb_item = self.dynamodb_client.get_item(
                TableName=self.table_name, Key={"document_id": {"S": document_id}}
            )

            if "Item" not in dynamodb_item:
                return None

            return self._unmarshal_dynamodb_json(dynamodb_item["Item"])
        except Exception as e:
            raise DatabaseException(f"Failed to get the document {document_id}") from e

    def write_document(self, document: dict[str, Any]):
        dynamodb_item = self._convert_to_decimal(document)
        self.dynamodb_client.put_item(TableName=self.table_name, Item=dynamodb_item)
        # self.table.put_item(Item=document)

    def _unmarshal_dynamodb_json(self, dynamodb_data: dict[str, Any]) -> dict[str, Any]:
        """Converts DynamoDB JSON format to standard JSON using TypeDeserializer and handles Decimals."""
        deserialized_data = {k: self.deserializer.deserialize(v) for k, v in dynamodb_data.items()}
        return self._convert_from_decimal(deserialized_data)

    @staticmethod
    def _convert_from_decimal(value):
        """Recursively converts Decimal to float or int."""
        if isinstance(value, Decimal):
            return int(value) if value % 1 == 0 else float(value)
        elif isinstance(value, list):
            return [DynamoDb._convert_from_decimal(v) for v in value]
        elif isinstance(value, dict):
            return {k: DynamoDb._convert_from_decimal(v) for k, v in value.items()}
        return value

    @staticmethod
    def _convert_to_decimal(value):
        """Recursively converts float values in a dictionary to Decimal for DynamoDB compatibility."""
        if isinstance(value, float):
            return Decimal(str(value))
        elif isinstance(value, list):
            return [DynamoDb._convert_to_decimal(i) for i in value]
        elif isinstance(value, dict):
            return {k: DynamoDb._convert_to_decimal(v) for k, v in value.items()}
        return value
