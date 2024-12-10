resource "aws_vpc" "vpc" {
  cidr_block = "172.2.0.0/16"
  tags = {
    Name = var.vpc_name
  }
}