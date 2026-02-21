resource "aws_emr_cluster" "lakehouse" {
  name          = "${var.project}-${var.environment}-emr"
  release_label = "emr-7.1.0"

  applications = ["Spark", "Hive", "JupyterEnterpriseGateway"]

  ec2_attributes {
    instance_profile = aws_iam_instance_profile.emr.arn
  }

  master_instance_group {
    instance_type = "m5.xlarge"
  }

  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 2
  }

  tags = {
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_iam_role" "emr" {
  name = "${var.project}-${var.environment}-emr-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "elasticmapreduce.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "emr" {
  name = "${var.project}-${var.environment}-emr-profile"
  role = aws_iam_role.emr.name
}

variable "project"     { type = string }
variable "environment" { type = string }
