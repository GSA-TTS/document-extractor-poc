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
    region = "us-east-1"
  }
}

locals {
  project = "document-extractor"
}

data "aws_caller_identity" "current" {}
