import json
import os

import boto3

bedrock_client = boto3.client("bedrock-runtime")

DOCUMENT_CLASSIFICATION_PROMPT = os.environ.get("DOCUMENT_CLASSIFICATION_PROMPT")
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID")


def lambda_handler(event, context):
    """Classifies a document using Amazon Bedrock API with structured JSON input"""
    try:
        print(event)
        document_data = event.get("extracted_data", {})
        print(document_data)
        if not document_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No document data provided."}),
            }

        formatted_document = json.dumps(document_data, indent=2)

        classification_prompt = DOCUMENT_CLASSIFICATION_PROMPT.format(document_text=formatted_document)

        # Call Amazon Bedrock
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"prompt": classification_prompt}),
        )

        # response
        response_body = json.loads(response["body"].read().decode("utf-8"))
        classification = response_body["completion"].strip()

        return {
            "statusCode": 200,
            "body": json.dumps({"document_type": classification}),
        }

    except Exception as e:
        print(f"❌ Error in classification: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
