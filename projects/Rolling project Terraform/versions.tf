terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.17.0"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.1.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "~> 2.5.3"
    }

    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.4"
    }
  }
}
