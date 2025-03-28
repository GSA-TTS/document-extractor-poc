module "document_endpoints" {
  source = "./endpoint"

  api_gateway_name = aws_api_gateway_rest_api.api.name

  handler_method_mapping = [
    {
      name              = "create-document"
      handler_file_path = local.lambda_filename
      handler_package   = "src.external.aws.lambdas.s3_file_upload.lambda_handler"
      http_method       = "POST"
    },
  ]

  resource_prefix       = "${local.project}-${var.environment}"
  path_part             = "document"
  resource_parent_id    = aws_api_gateway_rest_api.api.root_resource_id
  lambda_execution_role = aws_iam_role.execution_role.arn
  kms_key_arn           = aws_kms_key.encryption.arn

  environment_variables = {
    S3_BUCKET_NAME = aws_s3_bucket.document_storage.bucket
  }

  depends_on = [aws_api_gateway_rest_api.api]
}

module "document_id_endpoints" {
  source = "./endpoint"

  api_gateway_name = aws_api_gateway_rest_api.api.name

  handler_method_mapping = [
    {
      name              = "get-document"
      handler_file_path = local.lambda_filename
      handler_package   = "src.external.aws.lambdas.get_extracted_document.lambda_handler"
      http_method       = "GET"
    },
    {
      name              = "update-document"
      handler_file_path = local.lambda_filename
      handler_package   = "src.external.aws.lambdas.update_extracted_document.lambda_handler"
      http_method       = "PUT"
    },
  ]

  resource_prefix       = "${local.project}-${var.environment}"
  path_part             = "{document_id}"
  resource_parent_id    = module.document_endpoints.resource_id
  lambda_execution_role = aws_iam_role.execution_role.arn
  kms_key_arn           = aws_kms_key.encryption.arn

  environment_variables = {
    DYNAMODB_TABLE = aws_dynamodb_table.extract_table.name
    S3_BUCKET      = aws_s3_bucket.document_storage.bucket
  }

  depends_on = [aws_api_gateway_rest_api.api]
}
