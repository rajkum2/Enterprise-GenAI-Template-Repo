terraform {
  required_version = ">= 1.5.0"
}

# OpenSearch stub
resource "aws_opensearch_domain" "this" {
  domain_name = "genai-opensearch"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type = "t3.small.search"
  }
}
