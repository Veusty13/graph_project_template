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
      "Action": [     
        "s3:PutObject",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::project-bucket/*"]
    }
    ]
  })
}

data "aws_iam_policy_document" "feed_table_queue" {
  policy_id = "${aws_sqs_queue.feed_table_queue.arn}/SQSAccess"

  statement {
    sid    = "ConsumerAccess"
    effect = "Allow"
    actions = [
      "SQS:ReceiveMessage",
      "SQS:DeleteMessage",
      "SQS:GetQueueUrl",
    ]
    resources = [
      aws_sqs_queue.feed_table_queue.arn,
    ]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"

      values = [
        aws_lambda_function.feed_table_function.arn
      ]
    }
  }
  statement {
    sid    = "ProducerAccess"
    effect = "Allow"
    actions = [
      "SQS:SendMessage"
    ]
    resources = [
    aws_sqs_queue.feed_table_queue.arn]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"

      values = [
        aws_s3_bucket.project_bucket.arn
      ]
    }
  }
}