output "account_id" {
  description = "AWS account receiving the Café 53 resources."
  value       = data.aws_caller_identity.current.account_id
}

output "api_endpoint" {
  description = "Base URL for the Café 53 HTTP API."
  value       = aws_apigatewayv2_api.orders.api_endpoint
}

output "cloudfront_url" {
  description = "Public Café 53 frontend URL."
  value       = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "orders_table_name" {
  description = "DynamoDB table used for Café 53 orders."
  value       = aws_dynamodb_table.orders.name
}

output "orders_queue_url" {
  description = "SQS queue that buffers OrderCreated events."
  value       = aws_sqs_queue.orders.url
}

output "orders_dlq_url" {
  description = "SQS dead-letter queue for failed order processing."
  value       = aws_sqs_queue.order_dlq.url
}

output "notification_topic_arn" {
  description = "SNS topic for processed order notifications."
  value       = aws_sns_topic.order_ready.arn
}

