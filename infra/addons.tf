# external-secrets 
# TODO: Add a policy to allow access to aws secrets manager
module "external_secrets_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "v2.0.0"

  name = "external-secrets"

  attach_external_secrets_policy     = true
  external_secrets_create_permission = true

  associations = {
    postmortem-eks = {
      cluster_name    = module.eks.cluster_name
      namespace       = "external-secrets-system"
      service_account = "external-secrets"
    }
  }
  tags = {
    Environment = "demo"
  }
}

# External Secrets Operator Helm deployment
resource "helm_release" "external_secrets" {
  name             = "external-secrets"
  repository       = "https://charts.external-secrets.io"
  chart            = "external-secrets"
  version          = "0.19.2" # Latest stable version
  namespace        = "external-secrets-system"
  create_namespace = true

  values = [
    yamlencode({
      serviceAccount = {
        create = true
        name   = "external-secrets"
        annotations = {
          "eks.amazonaws.com/role-arn" = module.external_secrets_pod_identity.iam_role_arn
        }
      }

      # Security context for pods
      securityContext = {
        fsGroup = 65534
      }

      # Pod security context
      podSecurityContext = {
        runAsNonRoot = true
        runAsUser    = 65534
        runAsGroup   = 65534
      }

      # Resource limits
      resources = {
        limits = {
          cpu    = "100m"
          memory = "128Mi"
        }
        requests = {
          cpu    = "10m"
          memory = "32Mi"
        }
      }

      # Enable webhook for validation
      webhook = {
        create = true
      }

      # Enable cert-controller for webhook certificates
      certController = {
        create = true
      }
    })
  ]

  depends_on = [
    module.external_secrets_pod_identity
  ]
}

# ClusterSecretStore for AWS Secrets Manager
resource "kubectl_manifest" "cluster_secret_store" {
  yaml_body = yamlencode({
    apiVersion = "external-secrets.io/v1"
    kind       = "ClusterSecretStore"
    metadata = {
      name = "aws-secrets-manager"
    }
    spec = {
      provider = {
        aws = {
          service = "SecretsManager"
          region  = var.aws_region
        }
      }
    }
  })

  depends_on = [
    helm_release.external_secrets,
    module.external_secrets_pod_identity
  ]
}

# Test ExternalSecret for youtube/demo
#resource "kubectl_manifest" "test_external_secret" {
#  yaml_body = yamlencode({
#    apiVersion = "external-secrets.io/v1"
#    kind       = "ExternalSecret"
#    metadata = {
#      name      = "youtube-demo-secret"
#      namespace = "default"
#    }
#    spec = {
#      refreshInterval = "1h"
#      secretStoreRef = {
#        name = "aws-secrets-manager"
#        kind = "ClusterSecretStore"
#      }
#      target = {
#        name           = "youtube-demo"
#        creationPolicy = "Owner"
#        type           = "Opaque"
#      }
#      data = [
#        {
#          secretKey = "api-key"
#          remoteRef = {
#            key      = "youtube/demo"
#            property = "api-key"
#          }
#        }
#      ]
#    }
#  })
#
#  depends_on = [
#    kubectl_manifest.cluster_secret_store
#  ]
#}

