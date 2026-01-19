terraform {
  required_version = ">= 1.5.0"
}

# Redis stub
resource "aws_elasticache_cluster" "this" {
  cluster_id           = "genai-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
}
