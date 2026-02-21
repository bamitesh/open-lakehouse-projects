output "bronze_bucket_name" {
  description = "S3 bucket name for the Bronze layer."
  value       = module.storage.bronze_bucket_name
}

output "silver_bucket_name" {
  description = "S3 bucket name for the Silver layer."
  value       = module.storage.silver_bucket_name
}

output "gold_bucket_name" {
  description = "S3 bucket name for the Gold layer."
  value       = module.storage.gold_bucket_name
}
