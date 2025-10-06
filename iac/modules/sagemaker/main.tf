provider "aws" {
  region = var.aws_region
  default_tags {
    tags = var.tags
  }
}

data "aws_caller_identity" "current" {}

locals {
  instance_id             = element(split("/", var.instance_arn), 1)
  sagemaker_account_prefix = "arn:aws:sagemaker:${var.aws_region}:${data.aws_caller_identity.current.account_id}"
}

########################################
# Bucket para modelos (sin versionado)
########################################
resource "aws_s3_bucket" "model_bucket" {
  bucket = "${var.owner}-sagemaker-models"

  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket_public_access_block" "model_bucket_block" {
  bucket                  = aws_s3_bucket.model_bucket.id
  block_public_acls        = true
  block_public_policy      = true
  ignore_public_acls       = true
  restrict_public_buckets  = true
}

########################################
# Rol y permisos para EC2
########################################
resource "aws_iam_role" "ec2_sagemaker_role" {
  name = "${var.owner}-ec2-sagemaker-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "ec2.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "ec2_sagemaker_minimal_policy" {
  name        = "${var.owner}-ec2-sagemaker-policy"
  description = "Permisos mínimos: crear entrenamiento, inferencia e interactuar con S3 y SageMaker."
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid = "SageMakerTrainInfer",
        Effect = "Allow",
        Action = [
          "sagemaker:CreateTrainingJob",
          "sagemaker:DescribeTrainingJob",
          "sagemaker:ListTrainingJobs",
          "sagemaker:StopTrainingJob",
          "sagemaker:InvokeEndpoint",
          "sagemaker:DescribeEndpoint",
          "sagemaker:ListEndpoints"
        ],
        Resource = "*"
      },
      {
        Sid = "S3ReadOnlyResults",
        Effect = "Allow",
        Action = ["s3:ListBucket"],
        Resource = [aws_s3_bucket.model_bucket.arn]
      },
      {
        Sid = "S3GetObjects",
        Effect = "Allow",
        Action = ["s3:GetObject"],
        Resource = ["${aws_s3_bucket.model_bucket.arn}/*"]
      },
      {
        Sid = "AllowLogsDescribe",
        Effect = "Allow",
        Action = [
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents"
        ],
        Resource = "*"
      },
      {
        Sid = "PassSageMakerExecRole",
        Effect = "Allow",
        Action = ["iam:PassRole"],
        Resource = [aws_iam_role.sagemaker_execution_role.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_ec2_policy" {
  role       = aws_iam_role.ec2_sagemaker_role.name
  policy_arn = aws_iam_policy.ec2_sagemaker_minimal_policy.arn
}

resource "aws_iam_instance_profile" "ec2_sagemaker_instance_profile" {
  name = "${var.owner}-ec2-sagemaker-profile"
  role = aws_iam_role.ec2_sagemaker_role.name
}

resource "aws_iam_instance_profile_association" "associate_profile_to_instance" {
  instance_id          = local.instance_id
  iam_instance_profile = aws_iam_instance_profile.ec2_sagemaker_instance_profile.arn
}

########################################
# Rol de ejecución para SageMaker
########################################
resource "aws_iam_role" "sagemaker_execution_role" {
  name = "${var.owner}-sagemaker-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "sagemaker.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "sagemaker_exec_minimal_policy" {
  name        = "${var.owner}-sagemaker-exec-policy"
  description = "Permisos mínimos para SageMaker (S3 y logs)"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid = "S3AccessForSageMaker",
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.model_bucket.arn,
          "${aws_s3_bucket.model_bucket.arn}/*"
        ]
      },
      {
        Sid = "CloudWatchLogs",
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },
      {
        Sid = "ECRReadAccess",
        Effect = "Allow",
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_sagemaker_exec_policy" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = aws_iam_policy.sagemaker_exec_minimal_policy.arn
}

resource "aws_ecr_repository" "training_repo" {
  name                 = "${var.owner}-sagemaker-training"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}
