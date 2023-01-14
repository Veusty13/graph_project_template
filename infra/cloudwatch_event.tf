resource "aws_cloudwatch_event_rule" "trigger_processing_function" {
  name                = "trigger-processing-function"
  description         = "Triggers lambda in charge of triggering data processing"
  schedule_expression = var.trigger_expression
}

resource "aws_cloudwatch_event_target" "start_trigger_processing_function" {
  rule = aws_cloudwatch_event_rule.trigger_processing_function.id
  arn  = aws_lambda_function.trigger_processing_function.arn
}