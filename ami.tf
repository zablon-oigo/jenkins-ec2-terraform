data "aws_ami" "ami" {
  most_recent = true
  filter {
    name   = "tag:Name"
    values = ["Jenkins-EC2"]
  }

}