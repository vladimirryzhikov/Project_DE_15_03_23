terraform {
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

  region = var.region
  #"eu-north-1"

}

resource "aws_instance" "A-01" {

  ami = var.ami
  #"ami-09e1162c87f73958b"
  instance_type = var.instance_type
  #"t3.micro"

  network_interface {
    network_interface_id = var.network_interface_id
    device_index         = 0
  }

  tags = {
    Name = var.instance_name
  }
}
