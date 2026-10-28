variable "aws_region" {
  description = "AWS Region used for regional Café 53 resources."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Short environment name used in resource names and tags."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be dev, test, or prod."
  }
}

variable "project_name" {
  description = "Project identifier used for naming and tagging."
  type        = string
  default     = "cafe-53"
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention period."
  type        = number
  default     = 14
}

variable "monthly_budget_usd" {
  description = "Monthly AWS cost budget in USD. This is not a hard spending cap."
  type        = number
  default     = 10

  validation {
    condition     = var.monthly_budget_usd >= 1
    error_message = "monthly_budget_usd must be at least 1."
  }
}

variable "budget_alert_email" {
  description = "Email address that receives AWS Budget notifications."
  type        = string
  sensitive   = true

  validation {
    condition     = can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.budget_alert_email))
    error_message = "budget_alert_email must be a valid email address."
  }
}

variable "enable_point_in_time_recovery" {
  description = "Enable DynamoDB point-in-time recovery for the learning environment."
  type        = bool
  default     = true
}

