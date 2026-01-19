terraform {
  required_version = ">= 1.5.0"
}

# IAM stub for IRSA roles and policies
resource "aws_iam_role" "service" {
  name = "genai-service-role"
  assume_role_policy = "CHANGE_ME"
}
