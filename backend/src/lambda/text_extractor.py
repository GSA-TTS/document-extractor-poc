import json
import os

import boto3

s3_client = boto3.client("s3")
textract_client = boto3.client("textract")
sqs_client = boto3.client("sqs")

SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket_name = record["s3"]["bucket"]["name"]
    document_key = record["s3"]["object"]["key"]

    print(f"Processing file: s3://{bucket_name}/{document_key}")

    try:
        metadata = s3_client.head_object(Bucket=bucket_name, Key=document_key)
        print("S3 Metadata Retrieved Successfully:")
        print(metadata)

    except Exception as e:
        print(f"Failed to retrieve S3 object metadata: {e}")
        return {
            "statusCode": 403,
            "body": json.dumps(
                "Failed to access S3 object. Check permissions or other issues with file or configurations."
            ),
        }

    try:
        print("Attempting AnalyzeDocument (Structured Mode)...")
        response = textract_client.analyze_document(
            Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}},
            FeatureTypes=["FORMS", "TABLES"],
        )
        extracted_data = parse_textract_response(response)

        # Check if AnalyzeDocument works
        if not extracted_data:
            print("AnalyzeDocument yielded no data. Falling back to DetectDocumentText...")
            response = textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}}
            )
            extracted_data = parse_ocr_response(response)

    except Exception as e:
        print(f"AnalyzeDocument failed: {e}. Falling back to DetectDocumentText...")
        try:
            response = textract_client.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}}
            )
            extracted_data = parse_ocr_response(response)
        except Exception as ocr_error:
            print(f"OCR extraction also failed: {ocr_error}")
            return {
                "statusCode": 500,
                "body": json.dumps(f"Failed to process document: {ocr_error}"),
            }

    print(f"Extracted Data: {json.dumps(extracted_data, indent=2)}")

    # Send extracted data to SQS
    try:
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(
                {
                    "document_key": document_key,
                    "extracted_data": extracted_data,
                }
            ),
        )
        print("Message sent to SQS successfully.")
    except Exception as sqs_error:
        print(f"Failed to send message to SQS: {sqs_error}")

    return {
        "statusCode": 200,
        "body": json.dumps("Document processed successfully and sent to SQS"),
    }


def parse_textract_response(response):
    """Parses structured data from AnalyzeDocument response into a simple key-value format."""
    extracted_data = {}
    block_map = {block["Id"]: block for block in response.get("Blocks", [])}

    # Extract form data
    for block in response.get("Blocks", []):
        if block["BlockType"] == "KEY_VALUE_SET" and "KEY" in block.get("EntityTypes", []):
            key_text, key_conf = get_text_from_block(block, block_map)
            value_text = ""
            for rel in block.get("Relationships", []):
                if rel["Type"] == "VALUE":
                    for value_id in rel["Ids"]:
                        value_block = block_map.get(value_id)
                        if value_block:
                            value_text, value_conf = get_text_from_block(value_block, block_map)
            if key_text:
                extracted_data[key_text] = {"value": value_text, "confidence": key_conf}

    return extracted_data


def parse_ocr_response(response):
    """Parses text from DetectDocumentText response with pseudo-keys based on content."""
    extracted_data = {}
    line_count = 1

    for block in response.get("Blocks", []):
        if block["BlockType"] == "LINE":
            line_text = block.get("DetectedText", "")
            confidence = block.get("Confidence", 0.0)

            # Generate a key based on the first 3 words
            words = line_text.split()[:3]
            key = "_".join(words).replace(":", "").replace(".", "").strip() or f"Line_{line_count}"

            # Ensure key uniqueness
            while key in extracted_data:
                key += f"_{line_count}"

            extracted_data[key] = {"value": line_text, "confidence": confidence}
            line_count += 1

    return extracted_data


def get_text_from_block(block, block_map):
    """Helper to extract text from a block."""
    text = ""
    confidence = block.get("Confidence", 0.0)
    if "Relationships" in block:
        for rel in block["Relationships"]:
            if rel["Type"] == "CHILD":
                for child_id in rel["Ids"]:
                    word_block = block_map.get(child_id)
                    if word_block and word_block.get("Text"):
                        text += word_block["Text"] + " "
    return text.strip(), confidence
