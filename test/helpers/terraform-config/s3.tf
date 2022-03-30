resource "aws_s3_bucket" "name" {
  bucket = "name"
  acl    = "log-delivery-write"

  lifecycle_rule {
    id      = "to_glacier"
    prefix  = ""
    enabled = true

    expiration {
      // much more comments
      days = 365
    }

    transition = {
      # way more comments
      days          = 30
      storage_class = "GLACIER"
    }
    # some comment
  }

  versioning {
    # more comments
    enabled = true
  }
}

module "bucket_name" {
  source = "s3_bucket_name"

  name    = "audit"
  account = var.account
  region  = var.region
}
