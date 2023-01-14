variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "us-east-1"
}

variable "trigger_expression" {
  description = "trigger lambda function in charge of triggering data processing"
  type = string
  # every 3 minutes
  default = "cron(0/3 * * * ? *)"
}