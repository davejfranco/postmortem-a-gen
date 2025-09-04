data "aws_iam_policy_document" "ecr" {
  statement {
    sid    = "new policy"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [data.aws_caller_identity.current.account_id]
    }

    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeRepositories",
      "ecr:GetRepositoryPolicy",
      "ecr:ListImages",
      "ecr:DeleteRepository",
      "ecr:BatchDeleteImage",
      "ecr:SetRepositoryPolicy",
      "ecr:DeleteRepositoryPolicy",
    ]
  }
}

resource "aws_ecr_repository_policy" "ecr" {
  repository = aws_ecr_repository.this.name
  policy     = data.aws_iam_policy_document.ecr.json
}

data "aws_iam_policy_document" "bedrock_policy" {
  statement {
    effect = "Allow"

    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "bedrock_invoke" {
  name   = "bedrock-invoke-policy"
  policy = data.aws_iam_policy_document.bedrock_policy.json
}

module "postmortem_access" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "v2.0.0"

  name = "${var.project_name}-access"

  additional_policy_arns = {
    additional           = aws_iam_policy.bedrock_invoke.arn
  }

  associations = {
    postmortem-eks = {
      cluster_name    = module.eks.cluster_name
      namespace       = "default"
      service_account = "${var.project_name}-sa"
    }
  }

  tags = {
    Environment = "demo"
  }
}


