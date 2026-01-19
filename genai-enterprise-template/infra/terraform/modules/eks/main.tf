terraform {
  required_version = ">= 1.5.0"
}

# EKS stub
resource "aws_eks_cluster" "this" {
  name     = "genai-eks"
  role_arn = "CHANGE_ME"

  vpc_config {
    subnet_ids = ["CHANGE_ME"]
  }
}
