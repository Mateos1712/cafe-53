import json
import os
from datetime import datetime, timezone

import boto3


sns = boto3.client("sns")
topic_arn = os.environ["TOPIC_ARN"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def parse_eventbridge_message(record):
    envelope = json.loads(record["body"])
    detail = envelope.get("detail", {})
    required = {"orderId", "customerName", "item", "size"}
    if not required.issubset(detail):
        raise ValueError("order event is missing required fields")
    return detail


def lambda_handler(event, _context):
    failures = []
    for record in event.get("Records", []):
        message_id = record.get("messageId", "unknown")
        try:
            order = parse_eventbridge_message(record)
            notification = {
                "eventType": "OrderReady",
                "orderId": order["orderId"],
                "customerName": order["customerName"],
                "item": order["item"],
                "size": order["size"],
                "status": "READY",
            }
            table.update_item(
                Key={"orderId": order["orderId"]},
                UpdateExpression="SET #status = :status, processedAt = :processed_at",
                ExpressionAttributeNames={"#status": "status"},
                ExpressionAttributeValues={
                    ":status": "READY",
                    ":processed_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            sns.publish(
                TopicArn=topic_arn,
                Subject="Café 53 order ready",
                Message=json.dumps(notification),
            )
            print(json.dumps({"level": "INFO", **notification}))
        except Exception:
            print(json.dumps({"level": "ERROR", "messageId": message_id, "message": "order processing failed"}))
            failures.append({"itemIdentifier": message_id})

    return {"batchItemFailures": failures}

