################################
# REQUIRED VARS (correct syntax)
################################

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_id" {
  type    = string
  default = "vpc-0b110d239f1211b4d"
}

variable "public_subnet_id" {
  type    = string
  default = "subnet-0852a4e422a2ea812"
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}

variable "instance_name" {
  type    = string
  default = "builder"
}

variable "allowed_cidr_ssh" {
  type    = string
  default = "87.70.37.166/32"
}

variable "allowed_cidr_app" {
  type    = string
  default = "87.70.37.166/32"
}

variable "ssh_key_name" {
  type    = string
  default = "builder-key"
}

variable "private_key_filename" {
  type    = string
  default = "builder_key.pem"
}

provider "aws" {
  region = var.aws_region
}


############################
# Validate subnet & VPC
############################

data "aws_subnet" "target" {
  id = var.public_subnet_id
}

locals {
  subnet_vpc_match = data.aws_subnet.target.vpc_id == var.vpc_id
}

# Optional guardrail: fail early if mismatch
resource "null_resource" "subnet_vpc_guard" {
  triggers = {
    expected_vpc = var.vpc_id
    actual_vpc   = data.aws_subnet.target.vpc_id
  }

  lifecycle {
    precondition {
      condition     = local.subnet_vpc_match
      error_message = "The provided subnet (${data.aws_subnet.target.id}) is not in VPC ${var.vpc_id} (it is in ${data.aws_subnet.target.vpc_id})."
    }
  }
}

############################
# AMI lookup (Ubuntu)
############################

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

############################
# SSH key pair generation
############################

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key" {
  content         = tls_private_key.ssh_key.private_key_pem
  filename        = "${path.module}/${var.private_key_filename}"  
  file_permission = "0600"
}

resource "aws_key_pair" "builder_key" {
  key_name   = var.ssh_key_name
  public_key = tls_private_key.ssh_key.public_key_openssh
}

############################
# Security Group
############################

resource "aws_security_group" "builder_sg" {
  name_prefix = "builder-nikita-sg-"
  description = "Allow SSH (22) and app (5001)"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr_ssh]
  }

  ingress {
    description = "App port 5001"
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr_app]
  }

  egress {
    description      = "All outbound"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "builder-nikita-sg"
  }
}


############################
# EC2 Instance (Ubuntu)
############################

resource "aws_instance" "builder" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [aws_security_group.builder_sg.id]
  key_name                    = aws_key_pair.builder_key.key_name
  associate_public_ip_address = true

  # Optional: install Docker automatically on Ubuntu
  user_data = <<-EOF
              #!/bin/bash
              set -euxo pipefail
              apt-get update -y
              apt-get install -y ca-certificates curl gnupg lsb-release
              install -m 0755 -d /etc/apt/keyrings
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
              echo \
                "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
              apt-get update -y
              apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
              systemctl enable docker
              systemctl start docker
              usermod -aG docker ubuntu || true
              EOF

  tags = {
    Name = var.instance_name
  }
}
