resource "aws_sqs_queue" "feed_table_queue" {
  depends_on = [
    aws_sqs_queue.feed_table_error_queue
  ]

  name = "feed-table-queue"
  redrive_policy = jsonencode(
    {
      deadLetterTargetArn = aws_sqs_queue.feed_table_error_queue.arn
      maxReceiveCount = 2
    }
  )
}

resource "aws_sqs_queue" "feed_table_error_queue" {
  name = "feed-table-error-queue"
}

resource "aws_sqs_queue_policy" "feed_table_queue" {
  queue_url = aws_sqs_queue.feed_table_queue.id
  policy    = data.aws_iam_policy_document.feed_table_queue.json
}