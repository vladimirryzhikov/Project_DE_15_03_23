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
  type = string
  #default = "ami-0d32f1e246a0306ec"
  default = "ami-09e1162c87f73958b"

}




## EC2 instance type
variable "instance_type" {
  description = "Instance type for EMR and EC2"
  type        = string
  default     = "t3.micro"
}


variable "aws_region" {
  type    = string
  default = "eu-north-1"

}


## Key to allow connection to our EC2 instance
variable "key_name" {
  description = "EC2 key name"
  type        = string
  default     = "sde-key"
}


## Alert email receiver
variable "alert_email_id" {
  description = "Email id to send alerts to "
  type        = string
  default     = "vladimirryzhikov@icloud.com"
}


