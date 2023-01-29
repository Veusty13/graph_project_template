
provider "aws" {
  region = var.aws_region
  skip_credentials_validation = true
  skip_requesting_account_id = true
  skip_metadata_api_check = true
  s3_use_path_style = true

  endpoints {
    apigateway = "http://graph-project-local-stack:4566"
    iam = "http://graph-project-local-stack:4566"
    lambda = "http://graph-project-local-stack:4566"
    s3 = "http://graph-project-local-stack:4566"
    sns = "http://graph-project-local-stack:4566"
    sqs = "http://graph-project-local-stack:4566"
    cloudwatch ="http://graph-project-local-stack:4566"
    cloudwatchlogs ="http://graph-project-local-stack:4566"
    cloudwatchevents = "http://graph-project-local-stack:4566"
  }
}