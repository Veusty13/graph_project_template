resource "aws_s3_bucket" "project_bucket" {
  bucket = "project-bucket"
}

resource "aws_s3_bucket_notification" "feed_table_queue" {
  bucket = aws_s3_bucket.project_bucket.id

  queue {
    queue_arn     = aws_sqs_queue.feed_table_queue.arn
    filter_prefix = "processing/"
    filter_suffix = ".csv"
    events        = ["s3:ObjectCreated:*"]
  }
}
