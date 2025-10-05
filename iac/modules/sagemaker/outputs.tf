output "model_bucket_name" {
  value       = aws_s3_bucket.model_bucket.bucket
  description = "Nombre del bucket S3 para modelos"
}

output "model_bucket_arn" {
  value       = aws_s3_bucket.model_bucket.arn
  description = "ARN del bucket S3 para modelos"
}

output "ec2_role_arn" {
  value       = aws_iam_role.ec2_sagemaker_role.arn
  description = "ARN del rol asignado a la EC2"
}

output "sagemaker_execution_role_arn" {
  value       = aws_iam_role.sagemaker_execution_role.arn
  description = "ARN del rol que SageMaker usará en los training jobs"
}

output "training_repo_url" {
  value       = aws_ecr_repository.training_repo.repository_url
  description = "URL del repositorio ECR para imágenes de entrenamiento"
}

output "training_repo_arn" {
  value       = aws_ecr_repository.training_repo.arn
  description = "ARN del repositorio ECR para imágenes de entrenamiento"
}

