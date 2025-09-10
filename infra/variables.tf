variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "postmortems-reports"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

variable "cluster_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.33"
}

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access EKS API server"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "node_group_instance_types" {
  description = "Instance types for EKS node group"
  type        = list(string)
  default     = ["t3.large"]
}

variable "node_group_min_size" {
  description = "Minimum number of nodes in the node group"
  type        = number
  default     = 2
}

variable "node_group_max_size" {
  description = "Maximum number of nodes in the node group"
  type        = number
  default     = 4
}

variable "node_group_desired_size" {
  description = "Desired number of nodes in the node group"
  type        = number
  default     = 2
}

variable "slack_secrets" {
  description = "slack credentials"
  type = object({
    SLACK_BOT_TOKEN      = string
    SLACK_SIGNING_SECRET = string
    SLACK_CHANNEL_ID     = string
  })
  default = {
    SLACK_BOT_TOKEN      = ""
    SLACK_SIGNING_SECRET = ""
    SLACK_CHANNEL_ID     = ""
  }
}

variable "google_secrets" {
  description = "google secrets"
  type = object({
    GOOGLE_SERVICE_ACCOUNT_SUBJECT = string
    GOOGLE_FOLDER_ID               = string
    GOOGLE_CREDENTIALS_FILE        = string
    # To generate the credentials.json file
    GOOGLE_ACCESS_TYPE            = string
    GOOGLE_PROJECT_ID             = string
    GOOGLE_PRIVATE_KEY_ID         = string
    GOOGLE_PRIVATE_KEY            = string
    GOOGLE_CLIENT_EMAIL           = string
    GOOGLE_CLIENT_ID              = string
    GOOGLE_AUTH_URI               = string
    GOOGLE_TOKEN_URI              = string
    GOOGLE_AUTH_PROVIDER_CERT_URL = string
    GOOGLE_CLIENT_CERT_URL        = string
    GOOGLE_UNIVERSE_DOMAIN        = string
  })
  default = {
    GOOGLE_SERVICE_ACCOUNT_SUBJECT = ""
    GOOGLE_FOLDER_ID               = ""
    GOOGLE_CREDENTIALS_FILE        = ""
    # To generate the credentials.json file
    GOOGLE_ACCESS_TYPE            = ""
    GOOGLE_PROJECT_ID             = ""
    GOOGLE_PRIVATE_KEY_ID         = ""
    GOOGLE_PRIVATE_KEY            = ""
    GOOGLE_CLIENT_EMAIL           = ""
    GOOGLE_CLIENT_ID              = ""
    GOOGLE_AUTH_URI               = ""
    GOOGLE_TOKEN_URI              = ""
    GOOGLE_AUTH_PROVIDER_CERT_URL = ""
    GOOGLE_CLIENT_CERT_URL        = ""
    GOOGLE_UNIVERSE_DOMAIN        = ""
  }
}
