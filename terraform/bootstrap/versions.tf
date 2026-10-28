terraform {
  required_version = ">= 1.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "cafe-53"
      Environment = "shared"
      ManagedBy   = "Terraform"
      Purpose     = "Terraform-state"
    }
  }
}

