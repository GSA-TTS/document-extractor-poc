terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.94.1"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      project = "${local.project}-${var.environment}"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "document-extractor-terraform-state"
    key            = ""
    region         = "us-east-1"
    dynamodb_table = "terraform_lock"
  }
}

locals {
  project = "document-extractor"
}
