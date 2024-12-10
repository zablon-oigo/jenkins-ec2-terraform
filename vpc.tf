resource "aws_vpc" "vpc" {
  cidr_block = "172.2.0.0/16"
  tags = {
    Name = var.vpc_name
  }
}
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = var.igw_name
  }
}