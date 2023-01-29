 resource "aws_lambda_function" "feed_graph_function" {
  function_name = "feed-graph-function"

  s3_bucket = aws_s3_bucket.project_bucket.id
  s3_key    = aws_s3_object.lambda_zip.key

  runtime = "python3.8"
  handler = "feed_graph.lambda_handler"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_lambda_permission" "feed_graph_function" {
  statement_id  = "AllowExecutionOfFeedTableFunctionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.feed_graph_function.arn
  principal     = "sqs.amazonaws.com"
  source_arn    = aws_sqs_queue.feed_graph_queue.arn
}

resource "aws_lambda_event_source_mapping" "feed_graph_function" {
  event_source_arn = aws_sqs_queue.feed_graph_queue.arn
  function_name    = aws_lambda_function.feed_graph_function.arn
  batch_size       = 1
}