# Deployment evidence

## Current environment

- Environment: `dev`
- Region: `us-east-1`
- Frontend: <https://d3ujlt4nmaiwzc.cloudfront.net>
- Deployment date: October 27, 2026
- Terraform result: 36 application resources added, 0 changed, 0 destroyed
- Backend result: 4 protected state-bucket resources added
- Drift check after migration: `No changes`

## End-to-end verification

The deployed workload was verified through the public endpoints and AWS APIs:

1. `GET /health` returned `healthy`.
2. `POST /orders` returned HTTP 202 with a generated order ID.
3. DynamoDB contained the corresponding `RECEIVED` record.
4. EventBridge matched the `OrderCreated` event.
5. SQS delivered the message and returned to zero visible messages.
6. The worker Lambda logged an `OrderReady` event.
7. CloudFront returned HTTP 200 and loaded a generated API configuration.

## Cost and state controls

- Account-level monthly AWS Budget: USD 10.
- Forecast notification: greater than 80%.
- Actual-cost notification: greater than 100%.
- Terraform state: private S3 bucket with public access blocked, AES-256
  encryption, versioning and native S3 lock files.
- The bootstrap bucket has Terraform `prevent_destroy` protection.

AWS Budgets is an alerting mechanism, not a hard spending cap. The environment
should still be reviewed and destroyed when it is no longer required.

