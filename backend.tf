terraform {
  backend "s3" {
    bucket         = "jenkins-bucket"
    region         = "us-west-2"
    key            = "jenkins-server-terraform/terraform.tfstate"
    dynamodb_table = "lock-files"
    encrypt        = true
  }
}