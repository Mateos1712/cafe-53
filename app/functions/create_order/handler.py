import json
import os
import uuid
from datetime import datetime, timezone

import boto3


dynamodb = boto3.resource("dynamodb")
events = boto3.client("events")
table = dynamodb.Table(os.environ["TABLE_NAME"])
event_bus_name = os.environ["EVENT_BUS_NAME"]

ALLOWED_ITEMS = {"Espresso Route", "Lambda Latte", "SQS Cold Brew"}
ALLOWED_SIZES = {"small", "medium", "large"}


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def validate_order(payload):
    customer_name = str(payload.get("customerName", "")).strip()
    item = payload.get("item")
    size = payload.get("size")

    if not customer_name or len(customer_name) > 60:
        return None, "customerName is required and must be at most 60 characters"
    if item not in ALLOWED_ITEMS:
        return None, "item is not available"
    if size not in ALLOWED_SIZES:
        return None, "size is not available"

    return {"customerName": customer_name, "item": item, "size": size}, None


def lambda_handler(event, _context):
    route_key = event.get("routeKey", "")
    if route_key == "GET /health":
        return response(200, {"service": "cafe-53", "status": "healthy"})

    if route_key == "GET /orders/{orderId}":
        order_id = (event.get("pathParameters") or {}).get("orderId", "").strip()
        if not order_id:
            return response(400, {"message": "orderId is required"})

        result = table.get_item(Key={"orderId": order_id}, ConsistentRead=True)
        order = result.get("Item")
        if not order:
            return response(404, {"message": "order not found"})
        return response(200, order)

    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return response(400, {"message": "body must contain valid JSON"})

    order, error = validate_order(payload)
    if error:
        return response(400, {"message": error})

    order_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    record = {
        "orderId": order_id,
        "createdAt": created_at,
        "status": "RECEIVED",
        **order,
    }

    try:
        table.put_item(Item=record, ConditionExpression="attribute_not_exists(orderId)")
        result = events.put_events(
            Entries=[
                {
                    "Source": "cafe53.orders",
                    "DetailType": "OrderCreated",
                    "Detail": json.dumps(record),
                    "EventBusName": event_bus_name,
                }
            ]
        )
        if result.get("FailedEntryCount", 0):
            raise RuntimeError("EventBridge rejected the order event")
    except Exception:
        print(json.dumps({"level": "ERROR", "orderId": order_id, "message": "order persistence or event publication failed"}))
        return response(500, {"message": "order could not be processed"})

    print(json.dumps({"level": "INFO", "orderId": order_id, "status": "RECEIVED"}))
    return response(202, {"orderId": order_id, "status": "RECEIVED"})

