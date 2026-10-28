# CLF-C02 study map

Café 53 is a study aid, not a claim that the exam requires implementation.
Cloud Practitioner focuses on recognizing services, benefits, responsibilities,
cost models and common use cases.

| Exam concept | Café 53 evidence | Question to answer |
| --- | --- | --- |
| Regions and Availability Zones | Configurable AWS Region | What changes between a Region and an AZ? |
| Shared responsibility | Managed services plus application code | Who patches Lambda infrastructure? Who secures the function code? |
| IAM and least privilege | Separate Lambda roles and scoped policies | Why avoid AdministratorAccess? |
| Storage | S3 frontend bucket | When would EBS or EFS be more appropriate? |
| Compute | Lambda functions | When would EC2, ECS or Elastic Beanstalk be preferable? |
| Databases | DynamoDB on-demand table | When would RDS/Aurora be a better choice? |
| Networking and delivery | API Gateway and CloudFront | How do Route 53 and CloudFront differ? |
| Integration | EventBridge, SQS and SNS | Which service routes, buffers or fans out messages? |
| Monitoring and audit | CloudWatch logs, dashboard and alarms; CloudTrail planned | How do CloudWatch and CloudTrail differ? |
| Encryption | S3, SQS, SNS and DynamoDB encryption | What is encryption at rest vs. in transit? |
| Reliability | DLQ and DynamoDB PITR | What problem does each mechanism solve? |
| Pricing | Serverless pay-per-use resources and AWS Budget | Why does a budget not enforce a hard spending limit? |
| Infrastructure as code | Terraform modules and state | What are the benefits of repeatable provisioning? |

## Comparisons to study outside the deployment

- EC2 On-Demand, Savings Plans, Reserved Instances and Spot Instances.
- S3 storage classes and lifecycle transitions.
- RDS Multi-AZ versus read replicas.
- DynamoDB on-demand versus provisioned capacity.
- Security Groups versus network ACLs.
- AWS Shield Standard versus Shield Advanced versus AWS WAF.
- AWS Organizations, Control Tower and IAM Identity Center.
- Basic, Business and Enterprise Support plan capabilities.
- AWS Pricing Calculator, Cost Explorer, Budgets and Cost and Usage Reports.

