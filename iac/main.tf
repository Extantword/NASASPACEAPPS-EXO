terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }

  backend "s3" {
    bucket         = "exo-nasa"
    key            = "state/terraform.tfstate"
    region         = "us-east-2"
    encrypt        = true
    use_lockfile = true
  }

  required_version = ">= 1.2"
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}
