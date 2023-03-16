terraform {

  # Cloud cinfig to be removed credentials for production(could be changed in real
  # cloud version of terraform.cloud)
  cloud {
    organization = "Sniper_il_projects"

    workspaces {
      name = "Test"
    }
  }

  required_providers {

    aws = {

      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}



provider "aws" {

  region = var.aws_region
  #"eu-north-1"

}

#resource "aws_instance" "A-01" {

#ami = var.ami
#"ami-09e1162c87f73958b"
#instance_type = var.instance_type
#"t3.micro"

/* network_interface {
    network_interface_id = var.network_interface_id
    device_index         = 0
  } */

/* tags = {
    Name = var.instance_name
  }
}
 */

# to edit
resource "aws_security_group" "my_security_group" {
  name        = "My_security_group"
  description = "Security group to allow inbound & outbound 8080 connections"

  ingress {
    description = "Inbound SCP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "My_security_group"
  }
}

# Create EC2 with IAM role to allow full S3 access and security group 
# Generate key par
resource "tls_private_key" "pr_key" {
  algorithm = "RSA"
  rsa_bits  = 4096

}

resource "aws_key_pair" "generated_key" {
  key_name_prefix = var.key_name
  public_key      = tls_private_key.pr_key.public_key_openssh

  /* provisioner "local-exec" { # Create a "myKey.pem" to your computer!!
    command = "echo '${tls_private_key.pr_key.private_key_pem}' > ./myKey.pem"
  } */
}
/* # write the private key generated to local file
resource "local_sensitive_file" "ssh_key" {
  #filename = "${ssh}/p1.pem"
  filename        = "key.pem"
  content         = tls_private_key.pr_key.private_key_pem
  file_permission = "0400"

}
resource "local_file" "ssh_key" {
  content  = tls_private_key.pr_key.private_key_pem
  filename = "key_local.pem"
  #file_permission = "0400"

}
 */ data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230208"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  # owners = ["483247834648"] # account id
}

resource "aws_instance" "A_01" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  key_name        = aws_key_pair.generated_key.key_name
  security_groups = [aws_security_group.my_security_group.name]
  tags = {
    Name = "A_01"

  }

  # ADD Setup here 
  user_data = <<EOF
  !/bin/bash

  echo "____________START SETUP____"
  echo "its been setup here someday"
  echo " replace with comands to install software"
  echo "____________END SETUP______"

  EOF
}
