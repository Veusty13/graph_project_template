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

resource "aws_sqs_queue" "feed_graph_queue" {
  depends_on = [
    aws_sqs_queue.feed_graph_error_queue
  ]

  name = "feed-graph-queue"
  redrive_policy = jsonencode(
    {
      deadLetterTargetArn = aws_sqs_queue.feed_graph_error_queue.arn
      maxReceiveCount = 2
    }
  )
}

resource "aws_sqs_queue" "feed_graph_error_queue" {
  name = "feed-graph-error-queue"
}

resource "aws_sqs_queue_policy" "feed_graph_queue" {
  queue_url = aws_sqs_queue.feed_graph_queue.id
  policy    = data.aws_iam_policy_document.feed_graph_queue.json
}