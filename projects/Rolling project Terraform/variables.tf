################################
# Required inputs
################################

variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1" 
}

variable "vpc_id" {
  description = "Target VPC ID"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID in the target VPC"
  type        = string
}

################################
# Instance settings
################################

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "instance_name" {
  description = "EC2 Name tag"
  type        = string
  default     = "builder"
}

################################
# Network access
################################

variable "allowed_cidr_ssh" {
  description = "CIDR allowed to SSH :22"
  type        = string
}

variable "allowed_cidr_app" {
  description = "CIDR allowed to access port :5001"
  type        = string
}

################################
# SSH key generation
################################

variable "ssh_key_name" {
  description = "AWS key pair name to create"
  type        = string
  default     = "builder-key"
}

variable "private_key_filename" {
  description = "Local path to save the generated PEM"
  type        = string
  default     = "${path.module}/builder_key.pem"
}
