output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.A_01.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.A_01.public_ip
}

/* output "instance_network_interface_id" {
  value = aws_instance.A_01.primary_network_interface_id
}   */

output "aws_region" {
  description = "Region set for AWS"
  value       = var.aws_region
}

output "ec2_public_dns" {
  description = "EC2 public dns."
  value       = aws_instance.A_01.public_dns
}

output "private_key" {
  description = "EC2 private key."
  value       = tls_private_key.pr_key.private_key_pem
  sensitive   = true
}

output "public_key" {
  description = "EC2 public key."
  value       = tls_private_key.pr_key.public_key_openssh
}

/* output "local_sensitive_file" {

  description = "name_file_local"
  value       = local_sensitive_file.ssh_key.filename

} */

