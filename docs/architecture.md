# Café 53 architecture

## Order flow

1. CloudFront serves the static frontend from a private S3 bucket using Origin
   Access Control.
2. The browser sends `POST /orders` to an API Gateway HTTP API.
3. API Gateway invokes the `create_order` Lambda.
4. The function validates the payload, writes the order to DynamoDB and emits an
   `OrderCreated` event to a custom EventBridge bus.
5. An EventBridge rule sends matching events to SQS.
6. The `process_order` Lambda consumes SQS messages and publishes a normalized
   `OrderReady` notification to SNS.
7. CloudWatch stores application logs. SQS moves repeatedly failing messages to
   the dead-letter queue after the configured receive count.

## Design decisions

### HTTP API instead of REST API

HTTP API is sufficient for this MVP and keeps the configuration and cost lower.
REST API features such as usage plans can be explored later as a comparison.

### DynamoDB on-demand capacity

The workload is unpredictable and very small. On-demand capacity avoids
provisioning read/write units during a learning project.

### EventBridge plus SQS

EventBridge performs content-based routing while SQS buffers work and provides
durable retries. They solve different problems and are intentionally used
together.

### Private S3 origin

The bucket blocks public access. CloudFront reads objects using Origin Access
Control, demonstrating defense in depth rather than enabling S3 website hosting.

## Reliability and failure handling

- API Lambda failures return a generic 500 response and write details to logs.
- EventBridge retries target delivery according to AWS service behavior.
- SQS provides buffering and moves poison messages to the DLQ.
- DynamoDB point-in-time recovery is configurable and enabled by default.
- Lambda reserved concurrency is intentionally omitted in the MVP; account-level
  limits remain a safety boundary.

## Phase 2: Route 53

Use a subdomain such as `cafe53.example.com` rather than transferring or
modifying an existing production zone immediately. Phase 2 will add:

- an ACM certificate in `us-east-1`;
- DNS validation records;
- a CloudFront alternate domain name;
- Route 53 alias A and AAAA records;
- optionally, a separate API custom domain.

