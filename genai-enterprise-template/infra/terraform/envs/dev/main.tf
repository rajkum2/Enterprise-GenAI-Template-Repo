module "vpc" {
  source = "../../modules/vpc"
}

module "eks" {
  source = "../../modules/eks"
}

module "aurora" {
  source = "../../modules/aurora"
}

module "opensearch" {
  source = "../../modules/opensearch"
}

module "redis" {
  source = "../../modules/redis"
}

module "s3" {
  source = "../../modules/s3"
}

module "ecr" {
  source = "../../modules/ecr"
}

module "iam" {
  source = "../../modules/iam"
}
