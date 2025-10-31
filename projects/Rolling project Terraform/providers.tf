provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "infra-automation"
      Environment = "dev"
      Owner       = "nikita"
    }
  }
}
