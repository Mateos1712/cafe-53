resource "aws_cloudwatch_event_bus" "orders" {
  name = "${local.name_prefix}-orders"
}

resource "aws_sqs_queue" "order_dlq" {
  name                      = "${local.name_prefix}-orders-dlq"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true
}

resource "aws_sqs_queue" "orders" {
  name                       = "${local.name_prefix}-orders"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 345600
  receive_wait_time_seconds  = 10
  sqs_managed_sse_enabled    = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_cloudwatch_event_rule" "order_created" {
  name           = "${local.name_prefix}-order-created"
  description    = "Route Café 53 OrderCreated events to SQS"
  event_bus_name = aws_cloudwatch_event_bus.orders.name

  event_pattern = jsonencode({
    source      = ["cafe53.orders"]
    detail-type = ["OrderCreated"]
  })
}

resource "aws_cloudwatch_event_target" "orders_queue" {
  rule           = aws_cloudwatch_event_rule.order_created.name
  event_bus_name = aws_cloudwatch_event_bus.orders.name
  arn            = aws_sqs_queue.orders.arn
  target_id      = "Cafe53OrdersQueue"
}

data "aws_iam_policy_document" "orders_queue" {
  statement {
    sid     = "AllowEventBridgeSendMessage"
    actions = ["sqs:SendMessage"]
    resources = [
      aws_sqs_queue.orders.arn
    ]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_cloudwatch_event_rule.order_created.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "orders" {
  queue_url = aws_sqs_queue.orders.id
  policy    = data.aws_iam_policy_document.orders_queue.json
}

resource "aws_sns_topic" "order_ready" {
  name              = "${local.name_prefix}-order-ready"
  kms_master_key_id = "alias/aws/sns"
}

resource "aws_cloudwatch_log_group" "process_order" {
  name              = "/aws/lambda/${local.name_prefix}-process-order"
  retention_in_days = var.log_retention_days
}

data "archive_file" "process_order" {
  type        = "zip"
  source_file = "${path.module}/../app/functions/process_order/handler.py"
  output_path = "${path.module}/.terraform/process_order.zip"
}

resource "aws_iam_role" "process_order" {
  name               = "${local.name_prefix}-process-order"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "process_order" {
  statement {
    sid = "ConsumeOrders"
    actions = [
      "sqs:ChangeMessageVisibility",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ReceiveMessage"
    ]
    resources = [aws_sqs_queue.orders.arn]
  }

  statement {
    sid       = "PublishReadyNotifications"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.order_ready.arn]
  }

  statement {
    sid = "WriteLogs"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["${aws_cloudwatch_log_group.process_order.arn}:*"]
  }
}

resource "aws_iam_role_policy" "process_order" {
  name   = "${local.name_prefix}-process-order"
  role   = aws_iam_role.process_order.id
  policy = data.aws_iam_policy_document.process_order.json
}

resource "aws_lambda_function" "process_order" {
  function_name    = "${local.name_prefix}-process-order"
  role             = aws_iam_role.process_order.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.13"
  filename         = data.archive_file.process_order.output_path
  source_code_hash = data.archive_file.process_order.output_base64sha256
  timeout          = 20
  memory_size      = 256

  environment {
    variables = {
      TOPIC_ARN = aws_sns_topic.order_ready.arn
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.process_order,
    aws_iam_role_policy.process_order
  ]
}

resource "aws_lambda_event_source_mapping" "orders" {
  event_source_arn        = aws_sqs_queue.orders.arn
  function_name           = aws_lambda_function.process_order.arn
  batch_size              = 5
  function_response_types = ["ReportBatchItemFailures"]
}

