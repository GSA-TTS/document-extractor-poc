resource "aws_s3_bucket" "document_storage" {
  bucket = "${local.project}-${var.environment}-documents-${data.aws_caller_identity.current.account_id}"

  force_destroy = false
}

resource "aws_s3_bucket_notification" "notify_on_input_data" {
  bucket = aws_s3_bucket.document_storage.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.text_extract.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "input/"
  }

  depends_on = [aws_lambda_permission.allow_bucket_invoke]
}

resource "aws_s3_bucket" "website_storage" {
  bucket = "${local.project}-${var.environment}-website-${data.aws_caller_identity.current.account_id}"

  force_destroy = true
}

resource "aws_s3_bucket_website_configuration" "website_configuration" {
  bucket = aws_s3_bucket.website_storage.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

module "read_website_files" {
  source  = "hashicorp/dir/template"
  version = "~> 1.0.2"

  base_dir = "${path.root}/../ui/dist/"
}

resource "aws_s3_object" "website_files" {
  for_each = module.read_website_files.files

  bucket = aws_s3_bucket.website_storage.bucket
  key    = each.key
  source = each.value.source_path

  etag         = each.value.digests.md5
  content_type = each.value.content_type

  tags = {
    project = local.project
  }
}

resource "aws_s3_bucket_public_access_block" "allow_website_public" {
  bucket = aws_s3_bucket.website_storage.id

  block_public_acls       = true
  block_public_policy     = false
  ignore_public_acls      = true
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "attach_cloudfront_read" {
  bucket = aws_s3_bucket.website_storage.bucket
  policy = data.aws_iam_policy_document.cloudfront_read.json

  depends_on = [aws_s3_bucket_public_access_block.allow_website_public]
}

data "aws_iam_policy_document" "cloudfront_read" {
  statement {
    sid    = "CloudFrontReadGetObject"
    effect = "Allow"
    principals {
      identifiers = ["*"]
      type        = "AWS"
    }
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      "${aws_s3_bucket.website_storage.arn}/*",
      aws_s3_bucket.website_storage.arn
    ]
  }
}
