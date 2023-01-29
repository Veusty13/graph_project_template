 resource "aws_lambda_function" "trigger_processing_function" {
  function_name = "trigger-processing-function"

  s3_bucket = aws_s3_bucket.project_bucket.id
  s3_key    = aws_s3_object.lambda_zip.key

  runtime = "python3.9"
  handler = "trigger_processing_of_new_data.lambda_handler"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir  = "../lambda_package/"
  output_path = "../lambda_package.zip"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.project_bucket.id

  key    = "deployment_folder/lambda_package.zip"
  source = data.archive_file.lambda_zip.output_path

  etag = filemd5(data.archive_file.lambda_zip.output_path)
}

resource "aws_lambda_permission" "trigger-processing-function-allow-cloudwatch" {
  statement_id  = "AllowExecutionOfTriggerProcessingFunctionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.trigger_processing_function.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.trigger_processing_function.arn
}
