 resource "aws_lambda_function" "feed_table_function" {
  function_name = "feed-table-function"

  s3_bucket = aws_s3_bucket.project_bucket.id
  s3_key    = aws_s3_object.lambda_zip.key

  runtime = "python3.9"
  handler = "feed_table.lambda_handler"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_lambda_permission" "feed_table_function" {
  statement_id  = "AllowExecutionOfFeedTableFunctionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.feed_table_function.arn
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.feed_table_queue.arn
}

resource "aws_lambda_event_source_mapping" "feed_table_function" {
  event_source_arn = aws_sqs_queue.feed_table_queue.arn
  function_name    = aws_lambda_function.feed_table_function.arn
  batch_size       = 1
}