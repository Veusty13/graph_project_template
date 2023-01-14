
provider "aws" {
  region = var.aws_region
  skip_credentials_validation = true
  skip_requesting_account_id = true
  skip_metadata_api_check = true
  s3_use_path_style = true

  endpoints {
    apigateway = "http://localstack:4566"
    iam = "http://localstack:4566"
    lambda = "http://localstack:4566"
    s3 = "http://localstack:4566"
    sns = "http://localstack:4566"
    sqs = "http://localstack:4566"
    cloudwatch ="http://localstack:4566"
    cloudwatchlogs ="http://localstack:4566"
    cloudwatchevents = "http://localstack:4566"
  }
}