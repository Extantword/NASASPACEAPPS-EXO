# Networking

variable "my_ip_cidr" {
  description = "Tu IP en formato CIDR para permitir SSH (ej: 1.2.3.4/32)"
  type        = string
}

# Compute

variable "front_instance_type" {
  description = "Instance type para las EC2"
  type        = string
  default     = "t3.micro"
}

variable "back_instance_type" {
  description = "Instance type para las EC2"
  type        = string
  default     = "g4ad.xlarge"
}

# Project Config

variable "project_name" {
  description = "Prefix name for resources"
  type        = string
  default     = "astrofeel"
}

variable "owner" {
  description = "Owner tag"
  type        = string
  default     = "exo"
}

# Provider Config

variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
