terraform {
  required_version = ">= 1.5.0"
}

# Aurora stub
resource "aws_rds_cluster" "this" {
  cluster_identifier = "genai-aurora"
  engine            = "aurora-postgresql"
  master_username   = "CHANGE_ME"
  master_password   = "CHANGE_ME"
}
