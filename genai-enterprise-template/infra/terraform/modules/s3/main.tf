terraform {
  required_version = ">= 1.5.0"
}

resource "aws_s3_bucket" "documents" {
  bucket = "genai-documents-CHANGE_ME"
}

resource "aws_s3_bucket_versioning" "documents" {
  bucket = aws_s3_bucket.documents.id
  versioning_configuration {
    status = "Enabled"
  }
}
