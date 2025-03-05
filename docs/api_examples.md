# Example API Requests and Responses

## Upload Document

### Request

```http request
POST /api/document
```

```json
{
    "file_content": "<base64-encoded content of the uploaded file>",
    "file_name": "<name of the file>"
}
```

### Response

```json
{
    "message": "File uploaded successfully.",
    "documentId": "<random UUID>"
}
```

## Get Document

### Request

```http request
GET /api/document/<document ID>
```

### Response

```json
{
    "document_id": "<random UUID>",
    "document_key": "<file path>",
    "document_type": "<the type of document>",
    "signed_url": "<URL to temporarily allow you to download the document>",
    "base64_encoded_file": "<base64 encoding of the document>",
    "extracted_data": {
        "<key extracted from the document>": {
            "value": "<value extracted from the document>",
            "confidence": <decimal number 0 - 100 representing how confident the system is in the key and value being correct>
        }
        // ...more...
    }
}
```

## Update Document

### Request

```http request
PUT /api/document/<document ID>
```

```json
{
    "extracted_data": {
        "<key extracted from the document to update>": {
            "value": "<value extracted from the document to update>"
        }
        // ...more...
    }
}
```

### Response

```json
{
    "message": "Document updated successfully",
    "updated_document": {
        "document_id": "<random UUID>",
        "document_key": "<file path>",
        "document_type": "<the type of document>",
        "extracted_data": {
            "<key extracted from the document>": {
                "value": "<updated value extracted from the document>",
                "confidence": <decimal number 0 - 100 representing how confident the system is in the key and value being correct>
            }
            // ...more...
        }
    }
}
```
