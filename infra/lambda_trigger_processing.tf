resource "aws_lambda_function" "lambda" {
  function_name = "trigger-processing-function"

  s3_bucket = aws_s3_bucket.project_bucket.id
  s3_key    = aws_s3_object.lambda_zip.key

  runtime = "python3.9"
  handler = "function.trigger_processing_of_new_data.lambda_handler"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir  = "../src/"
  output_path = "../src/function.zip"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.project_bucket.id

  key    = "function.zip"
  source = data.archive_file.lambda_zip.output_path

  etag = filemd5(data.archive_file.lambda_zip.output_path)
}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    },
    {
      "Sid": "ListObjectsInBucket",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::project-bucket"]
    },
    {
      "Sid": "AllObjectActions",
      "Effect": "Allow",
      "Action": "s3:*Object",
      "Resource": ["arn:aws:s3:::project-bucket/*"]
    }
    ]
  })
}