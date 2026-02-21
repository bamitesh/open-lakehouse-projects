terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # Override via -backend-config or environment variables
    bucket = "lakehouse-terraform-state"
    key    = "lakehouse/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

module "storage" {
  source      = "./modules/storage"
  environment = var.environment
  project     = var.project_name
}

module "compute" {
  source      = "./modules/compute"
  environment = var.environment
  project     = var.project_name
}
