data "aws_availability_zones" "available" { state = "available" }

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = var.project_name
  cidr = var.vpc_cidr

  public_subnets   = var.public_subnet_cidrs
  private_subnets  = var.private_subnet_cidrs
  azs              = data.aws_availability_zones.available.names

  map_public_ip_on_launch = true

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_vpn_gateway = false

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
  }

  public_subnet_tags = {
    Type = "public"
  }

  private_subnet_tags = {
    Type = "private"
  }
}

resource "aws_ecr_repository" "this" {
  name                 = "${var.project_name}-${var.environment}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
  }
}

data "aws_caller_identity" "current" {}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "21.1.0"

  name               = var.project_name
  kubernetes_version = var.cluster_version

  # EKS Addons
  addons = {
    coredns = {}
    eks-pod-identity-agent = {
      before_compute = true
    }
    kube-proxy = {}
    vpc-cni = {
      # need it before trying to create node groups
      before_compute = true
    }
  }
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  authentication_mode                      = "API"
  endpoint_public_access                   = true
  enable_cluster_creator_admin_permissions = true
  endpoint_public_access_cidrs             = var.allowed_cidr_blocks

  eks_managed_node_groups = {
    example = {
      instance_types = var.node_group_instance_types

      min_size     = var.node_group_min_size
      max_size     = var.node_group_max_size
      desired_size = var.node_group_desired_size
    }
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
  }
}



# DNS 
data "aws_route53_zone" "main" {
  name = "daveops.sh"
}

resource "aws_route53_zone" "dev" {
  name = "dev.daveops.sh"
}


resource "aws_route53_record" "dev_ns" {
  allow_overwrite = true
  name            = "dev.daveops.sh"
  ttl             = 172800
  type            = "NS"
  zone_id         = data.aws_route53_zone.main.zone_id

  records = aws_route53_zone.dev.name_servers
}

# Secrets
resource "aws_secretsmanager_secret" "slack" {
  name = "${var.environment}-${var.project_name}/slack"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "slack" {
  secret_id = aws_secretsmanager_secret.slack.id
  secret_string = jsonencode(var.slack_secrets)
}

resource "aws_secretsmanager_secret" "google" {
  name = "${var.environment}-${var.project_name}/google"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "google" {
  secret_id = aws_secretsmanager_secret.google.id
  secret_string = jsonencode(var.google_secrets)
}
