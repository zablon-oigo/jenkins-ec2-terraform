variable "region" {
  description = "Default Region"
  default     = "us-west-2"
}
variable "vpc_name" {
  default = "test-vpc"
}
variable "igw_name" {
  default = "test-igw"
}
variable "iam_role_name" {
  default = "test-user-iam-role"
}
variable "instance_name" {
  default = "test-server"
}