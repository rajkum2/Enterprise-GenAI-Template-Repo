terraform {
  required_version = ">= 1.5.0"
  backend "s3" {
    bucket = "CHANGE_ME"
    key    = "genai/dev/terraform.tfstate"
    region = "CHANGE_ME"
  }
}

provider "aws" {
  region = "CHANGE_ME"
}
