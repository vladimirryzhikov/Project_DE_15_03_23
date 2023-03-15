output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.A_01.id_01
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.A_01.public_ip
}
