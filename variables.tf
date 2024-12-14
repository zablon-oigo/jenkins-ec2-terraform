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
variable "route_table_name" {
  default     = "test-rt"
}
variable "security_group_name" {
  default     = "test-sg"
}