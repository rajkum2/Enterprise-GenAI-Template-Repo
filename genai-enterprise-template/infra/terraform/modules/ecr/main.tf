terraform {
  required_version = ">= 1.5.0"
}

resource "aws_ecr_repository" "this" {
  name = "genai-service"
  image_scanning_configuration {
    scan_on_push = true
  }
}
