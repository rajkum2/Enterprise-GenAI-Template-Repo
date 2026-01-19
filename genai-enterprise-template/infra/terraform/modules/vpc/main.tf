terraform {
  required_version = ">= 1.5.0"
}

# VPC stub
resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "genai-vpc"
  }
}
