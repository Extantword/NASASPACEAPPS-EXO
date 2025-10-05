# --- Security Groups ---
# SG para la instancia pública: permitir solo SSH desde my_ip_cidr
resource "aws_security_group" "sg_public_ssh" {
  name        = "${var.project_name}-sg-public-ssh"
  description = "Allow SSH from my IP"
  vpc_id      = aws_vpc.this.id

  # Inbound: SSH solo desde mi IP (var.my_ip_cidr debe ser algo como "1.2.3.4/32")
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  # Egress: permitir salida a cualquier destino (ajusta si quieres más restricción)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-sg-public-ssh" }
}

resource "aws_security_group" "sg_private_http" {
  name        = "${var.project_name}-sg-private-http"
  description = "Allow HTTP inbound from public SG and SSH from my IP"
  vpc_id      = aws_vpc.this.id

  # Inbound: SSH solo desde mi IP (si quieres que también puedas SSH a la privada)
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  # Inbound: HTTP solo desde la security group pública
  ingress {
    description     = "HTTP from public instances (only from public SG)"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.sg_public_ssh.id]
  }

  # Egress: permitir salida a cualquier destino (ajusta si quieres más restricción)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-sg-private-http" }
}

# --- AMI: Amazon Linux 2 (x86_64) ---
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# --- EC2 Instances ---
# Public instance (in public subnet, with public IP)
resource "aws_instance" "public" {
  ami                         = data.aws_ami.amazon_linux_2.id
  instance_type               = var.front_instance_type
  subnet_id                   = aws_subnet.public.id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.sg_public_ssh.id]
  user_data                   = file("${path.module}/dat/front-user-data.sh")
  tags = {
    Name  = "${var.project_name}-instance-public"
    Owner = var.owner
  }
}

# Private instance (no public IP)
resource "aws_instance" "private" {
  ami                         = data.aws_ami.amazon_linux_2.id
  instance_type               = var.front_instance_type
  subnet_id                   = aws_subnet.private.id
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.sg_private_http.id]
  user_data                   = file("${path.module}/dat/front-user-data.sh") # cambiar despues de lo del free tier
  tags = {
    Name  = "${var.project_name}-instance-private"
    Owner = var.owner
  }
}
