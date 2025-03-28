locals {
  lambda_filename         = "${path.module}/../backend/dist/lambda.zip"
  lambda_source_code_hash = filebase64sha256(local.lambda_filename)
}

resource "aws_lambda_function" "text_extract" {
  function_name = "${local.project}-${var.environment}-text-extract"

  filename         = local.lambda_filename
  source_code_hash = local.lambda_source_code_hash

  handler = "src.external.aws.lambdas.text_extractor.lambda_handler"

  memory_size                    = 256
  timeout                        = 30
  runtime                        = "python3.13"
  reserved_concurrent_executions = -1
  publish                        = true

  architectures = ["arm64"]

  kms_key_arn = aws_kms_key.encryption.arn

  role = aws_iam_role.execution_role.arn

  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.queue_to_dynamo.url
    }
  }
}

resource "aws_lambda_permission" "allow_bucket_invoke" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.text_extract.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.document_storage.arn
}

resource "aws_lambda_provisioned_concurrency_config" "text_extract_concurrency" {
  function_name                     = aws_lambda_function.text_extract.function_name
  provisioned_concurrent_executions = 1
  qualifier                         = aws_lambda_function.text_extract.version
}

resource "aws_lambda_function" "write_to_dynamodb" {
  function_name = "${local.project}-${var.environment}-write-to-dynamodb"

  filename         = local.lambda_filename
  source_code_hash = local.lambda_source_code_hash

  handler = "src.external.aws.lambdas.sqs_dynamo_writer.lambda_handler"

  memory_size                    = 256
  timeout                        = 30
  runtime                        = "python3.13"
  reserved_concurrent_executions = -1
  publish                        = true

  architectures = ["arm64"]

  kms_key_arn = aws_kms_key.encryption.arn

  role = aws_iam_role.execution_role.arn

  environment {
    variables = {
      SQS_QUEUE_URL  = aws_sqs_queue.queue_to_dynamo.url
      DYNAMODB_TABLE = aws_dynamodb_table.extract_table.name
    }
  }
}

resource "aws_lambda_event_source_mapping" "invoke_dynamodb_writer_from_sqs" {
  event_source_arn                   = aws_sqs_queue.queue_to_dynamo.arn
  function_name                      = aws_lambda_function.write_to_dynamodb.arn
  maximum_batching_window_in_seconds = 0

  depends_on = [aws_iam_role_policy_attachment.attach_sqs_permission_to_role]
}

resource "aws_lambda_provisioned_concurrency_config" "write_to_dynamodb_concurrency" {
  function_name                     = aws_lambda_function.write_to_dynamodb.function_name
  provisioned_concurrent_executions = 1
  qualifier                         = aws_lambda_function.write_to_dynamodb.version
}
