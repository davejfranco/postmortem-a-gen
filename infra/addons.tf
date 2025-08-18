# external-secrets 
data "aws_iam_policy_document" "external_secrets_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["pods.eks.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
      "sts:TagSession"
    ]
  }
}

data "aws_iam_policy_document" "external_secrets" {
  statement {
    effect = "Allow"
    
    actions = [
      "secretsmanager:GetResourcePolicy",
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "secretsmanager:ListSecretVersionIds",
      "secretsmanager:ListSecrets"
    ]
    
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParametersByPath",
      "ssm:DescribeParameters"
    ]
    
    resources = ["*"]
  }
}

resource "aws_iam_role" "external_secrets" {
  name               = "${var.project_name}-external-secrets"
  assume_role_policy = data.aws_iam_policy_document.external_secrets_assume_role.json

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
  }
}

resource "aws_iam_policy" "external_secrets" {
  name   = "${var.project_name}-external-secrets"
  policy = data.aws_iam_policy_document.external_secrets.json

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
  }
}

resource "aws_iam_role_policy_attachment" "external_secrets" {
  role       = aws_iam_role.external_secrets.name
  policy_arn = aws_iam_policy.external_secrets.arn
}

resource "aws_eks_pod_identity_association" "external_secrets" {
  cluster_name    = module.eks.cluster_name
  namespace       = "external-secrets-system"
  service_account = "external-secrets"
  role_arn        = aws_iam_role.external_secrets.arn

  tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
  }
}

resource "helm_release" "external_secrets" {
  name       = "external-secrets"
  repository = "https://charts.external-secrets.io"
  chart      = "external-secrets"
  namespace  = "external-secrets-system"
  create_namespace = true

  version = "0.9.11"

  values = [
    yamlencode({
      installCRDs = true
      serviceAccount = {
        annotations = {
          "eks.amazonaws.com/role-arn" = aws_iam_role.external_secrets.arn
        }
      }
    })
  ]

  depends_on = [
    module.eks,
    aws_eks_pod_identity_association.external_secrets
  ]
}
# external-dns

# cert-manager 


