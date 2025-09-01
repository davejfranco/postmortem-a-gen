# external-secrets 
# TODO: Add a policy to allow access to aws secrets manager
module "external_secrets_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "v2.0.0"

  name = "external-secrets"

  attach_external_secrets_policy        = true
  external_secrets_secrets_manager_arns = ["arn:aws:secretsmanager:*:*:secret:*"]

  associations = {
    postmortem-eks = {
      cluster_name    = module.eks.cluster_name
      namespace       = "external-secrets"
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
  namespace        = "external-secrets"
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

      # Resource limits
      resources = {
        limits = {
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

# external-dns
module "external_dns_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "v2.0.0"

  name = "external-dns"

  attach_external_dns_policy    = true
  external_dns_hosted_zone_arns = [aws_route53_zone.dev.arn]

  associations = {
    postmortem-eks = {
      cluster_name    = module.eks.cluster_name
      namespace       = "external-dns"
      service_account = "external-dns"
    }
  }

  tags = {
    Environment = "demo"
  }
}

resource "helm_release" "external_dns" {
  name             = "external-dns"
  repository       = "https://kubernetes-sigs.github.io/external-dns/"
  chart            = "external-dns"
  version          = "1.18.0" # Latest stable version
  namespace        = "external-dns"
  create_namespace = true

  values = [
    yamlencode({
      serviceAccount = {
        create = true
        name   = "external-dns"
        annotations = {
          "eks.amazonaws.com/role-arn" = module.external_dns_pod_identity.iam_role_arn
        }
      }

      provider = "aws"
      aws = {
        region = var.aws_region
      }

      txtOwnerId = "postmortem"

      domainFilters = [aws_route53_zone.dev.name]

      # Resource limits
      resources = {
        limits = {
          memory = "128Mi"
        }
        requests = {
          cpu    = "10m"
          memory = "32Mi"
        }
      }

    })
  ]

  depends_on = [
    module.external_dns_pod_identity
  ]
}

# cert-manager
module "cert_manager_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "v2.0.0"

  name = "cert-manager"

  attach_cert_manager_policy    = true
  cert_manager_hosted_zone_arns = [aws_route53_zone.dev.arn]

  associations = {
    postmortem-eks = {
      cluster_name    = module.eks.cluster_name
      namespace       = "cert-manager"
      service_account = "cert-manager"
    }
  }
  
  tags = {
    Environment = "demo"
  }
}

resource "helm_release" "cert_manager" {
  name             = "cert-manager"
  repository       = "https://charts.jetstack.io"
  chart            = "cert-manager"
  version          = "1.18.2" # Latest stable version
  namespace        = "cert-manager"
  create_namespace = true

  values = [
    yamlencode({
      serviceAccount = {
        create = true
        name   = "cert-manager"
        annotations = {
          "eks.amazonaws.com/role-arn" = module.cert_manager_pod_identity.iam_role_arn
        }
      }

      installCRDs = true

      # Resource limits
      resources = {
        limits = {
          memory = "128Mi"
        }
        requests = {
          cpu    = "10m"
          memory = "32Mi"
        }
      }

    })
  ]

  depends_on = [
    module.cert_manager_pod_identity
  ]
}

# ClusterIssuer for Let's Encrypt
resource "kubectl_manifest" "letsencrypt_cluster_issuer" {
  yaml_body = yamlencode({
    apiVersion = "cert-manager.io/v1"
    kind       = "ClusterIssuer"
    metadata = {
      name = "letsencrypt-prod"
    }
    spec = {
      acme = {
        server = "https://acme-v02.api.letsencrypt.org/directory"
        email  = "admin@daveops.sh"
        privateKeySecretRef = {
          name = "letsencrypt-prod"
        }
        solvers = [
          {
            dns01 = {
              route53 = {
                region = var.aws_region
              }
            }
          }
        ]
      }
    }
  })

  depends_on = [
    helm_release.cert_manager
  ]
}
