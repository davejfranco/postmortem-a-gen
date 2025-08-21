module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = var.project_name
  cidr = var.vpc_cidr

  azs              = var.availability_zones
  public_subnets   = var.public_subnet_cidrs
  private_subnets  = var.private_subnet_cidrs
  database_subnets = var.database_subnet_cidrs

  map_public_ip_on_launch = true

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_vpn_gateway = false

  enable_dns_hostnames = true
  enable_dns_support   = true

  create_database_subnet_group       = true
  create_database_subnet_route_table = true

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

  database_subnet_tags = {
    Type = "database"
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
  version = "~> 21.0"

  name               = var.project_name
  kubernetes_version = var.cluster_version

  vpc_id                   = module.vpc.vpc_id
  control_plane_subnet_ids = module.vpc.public_subnets
  subnet_ids = concat(
    module.vpc.public_subnets,
    module.vpc.private_subnets
  )

  endpoint_public_access       = true
  endpoint_private_access      = true
  endpoint_public_access_cidrs = var.allowed_cidr_blocks

  addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    eks-pod-identity-agent = {
      most_recent = true
    }
  }
  authentication_mode = "API"
  # Enable cluster creator admin permissions
  enable_cluster_creator_admin_permissions = true

  # Access entries for additional users/roles
  access_entries = {
    cluster_creator = {
      principal_arn = data.aws_caller_identity.current.arn
      policy_associations = {
        admin = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }

  #eks_managed_node_groups = {
  #  main = {
  #    name = "nodes"

  #    instance_types = var.node_group_instance_types

  #    min_size     = var.node_group_min_size
  #    max_size     = var.node_group_max_size
  #    desired_size = var.node_group_desired_size

  #    subnet_ids = module.vpc.public_subnets

  #    tags = {
  #      Environment = var.environment
  #      Project     = var.project_name
  #      Terraform   = "true"
  #    }
  #  }
  #}

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

