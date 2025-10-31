################################
# Outputs
################################

# Public IP of your EC2
output "instance_public_ip" {
  value       = aws_instance.builder.public_ip
  description = "Public IP of the builder-nikita EC2 instance"
}

# Security group ID (optional)
output "security_group_id" {
  value       = aws_security_group.builder_sg.id
  description = "Security Group ID used by builder-nikita"
}

# Path to PEM file
output "ssh_private_key_path" {
  value       = "${path.module}/${var.private_key_filename}"
  description = "Path to the generated private key PEM file"
  sensitive   = true
}
