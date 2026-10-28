import importlib.util
import pathlib
import sys
import types
import unittest


class FakeTable:
    pass


fake_boto3 = types.SimpleNamespace(
    resource=lambda _name: types.SimpleNamespace(Table=lambda _table: FakeTable()),
    client=lambda _name: object(),
)
sys.modules.setdefault("boto3", fake_boto3)

import os
os.environ.setdefault("TABLE_NAME", "test-orders")
os.environ.setdefault("EVENT_BUS_NAME", "test-bus")

module_path = pathlib.Path(__file__).with_name("handler.py")
spec = importlib.util.spec_from_file_location("create_order_handler", module_path)
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)


class ValidateOrderTests(unittest.TestCase):
    def test_accepts_valid_order(self):
        order, error = handler.validate_order(
            {"customerName": "Andrea", "item": "Lambda Latte", "size": "medium"}
        )
        self.assertIsNone(error)
        self.assertEqual(order["customerName"], "Andrea")

    def test_rejects_unknown_item(self):
        order, error = handler.validate_order(
            {"customerName": "Andrea", "item": "Unknown", "size": "medium"}
        )
        self.assertIsNone(order)
        self.assertIn("not available", error)

    def test_rejects_blank_name(self):
        order, error = handler.validate_order(
            {"customerName": "  ", "item": "Lambda Latte", "size": "medium"}
        )
        self.assertIsNone(order)
        self.assertIn("customerName", error)


if __name__ == "__main__":
    unittest.main()

