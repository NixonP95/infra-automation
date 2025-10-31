########################################
# General
########################################

variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

########################################
# Networking
########################################

variable "vpc_id" {
  description = "Existing VPC ID to use"
  type        = string
  default     = "vpc-0b110d239f1211b4d"
}

variable "public_subnet_id" {
  description = "Public subnet (in the VPC) where the EC2 instance will be created"
  type        = string
  default     = "subnet-0852a4e422a2ea812"
}

########################################
# EC2 instance
########################################

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "instance_name" {
  description = "Name tag for the EC2 instance"
  type        = string
  default     = "builder-nikita"
}

########################################
# Security group / access
########################################

variable "allowed_cidr_ssh" {
  description = "CIDR block allowed to SSH into the instance (port 22)"
  type        = string
  # replace with your /32
  default     = "0.0.0.0/0"
}

variable "allowed_cidr_app" {
  description = "CIDR block allowed to access the app port (5001)"
  type        = string
  # replace with your /32
  default     = "0.0.0.0/0"
}

########################################
# SSH key management
########################################

variable "ssh_key_name" {
  description = "Name of the AWS key pair to create"
  type        = string
  default     = "builder-nikita-key"
}

variable "private_key_filename" {
  description = "Local filename to write the generated private key to"
  type        = string
  default     = "builder_nikita.pem"
}
