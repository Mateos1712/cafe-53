import importlib.util
import json
import os
import pathlib
import sys
import types
import unittest


class FakeTable:
    def update_item(self, **_kwargs):
        return {}


fake_boto3 = types.SimpleNamespace(
    client=lambda _name: object(),
    resource=lambda _name: types.SimpleNamespace(Table=lambda _table: FakeTable()),
)
sys.modules.setdefault("boto3", fake_boto3)
os.environ.setdefault("TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:test")
os.environ.setdefault("TABLE_NAME", "test-orders")

module_path = pathlib.Path(__file__).with_name("handler.py")
spec = importlib.util.spec_from_file_location("process_order_handler", module_path)
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)


class ParseMessageTests(unittest.TestCase):
    def test_parses_eventbridge_envelope(self):
        detail = {
            "orderId": "abc",
            "customerName": "Andrea",
            "item": "SQS Cold Brew",
            "size": "large",
        }
        result = handler.parse_eventbridge_message({"body": json.dumps({"detail": detail})})
        self.assertEqual(result, detail)

    def test_rejects_incomplete_event(self):
        with self.assertRaises(ValueError):
            handler.parse_eventbridge_message({"body": json.dumps({"detail": {"orderId": "abc"}})})


if __name__ == "__main__":
    unittest.main()

