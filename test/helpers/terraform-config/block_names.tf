resource aws_eks_cluster "eks_bad" {
  name = "bad-eks"
  role_arn = var.role_arn
  vpc_config {
    subnet_ids = []
    endpoint_public_access = true
  }


  encryption_config {
    provider {
      key_arn = var.key_arn
    }
    resources = []
  }

  #  doesn't exist, just for testing
  resource {
    data {
      some = "thing"
    }
  }
}
