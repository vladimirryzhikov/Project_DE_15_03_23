variable "instance_name" {
  description = "Value of the name tag for the EC2 instance"
  type        = string
  default     = "SampleInstance"
}

variable "network_interface_id" {
  type    = string
  default = "network_id_from_aws"

}

variable "ami" {
  type    = string
  default = "ami-09e1162c87f73958b"

}

variable "instance_type" {
  type    = string
  default = "t3.micro"

}

variable "region" {
  type    = string
  default = "eu-north-1"

}






