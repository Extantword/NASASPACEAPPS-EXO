variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "owner" {
  description = "Identificador del propietario que formará parte del nombre del bucket. El bucket será \"${var.owner}-sagemaker-models\""
  type        = string
}

variable "instance_arn" {
  description = "ARN de la instancia EC2 (p.ej. arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef0)"
  type        = string
}

variable "inference_image" {
  description = "URI de la imagen de inferencia en ECR (opcional — si vas a crear modelo/endpoint)"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Mapa de etiquetas que se aplicarán (se usan como default_tags del provider para no tener que ponerlas en cada recurso)."
  type        = map(string)
  default     = {}
}
