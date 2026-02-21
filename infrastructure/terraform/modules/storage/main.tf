resource "aws_s3_bucket" "bronze" {
  bucket = "${var.project}-${var.environment}-bronze"
  tags = {
    Layer       = "bronze"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_s3_bucket" "silver" {
  bucket = "${var.project}-${var.environment}-silver"
  tags = {
    Layer       = "silver"
    Environment = var.environment
    Project     = var.project
  }
}

resource "aws_s3_bucket" "gold" {
  bucket = "${var.project}-${var.environment}-gold"
  tags = {
    Layer       = "gold"
    Environment = var.environment
    Project     = var.project
  }
}

variable "project" { type = string }
variable "environment" { type = string }

output "bronze_bucket_name" { value = aws_s3_bucket.bronze.id }
output "silver_bucket_name" { value = aws_s3_bucket.silver.id }
output "gold_bucket_name"   { value = aws_s3_bucket.gold.id }
