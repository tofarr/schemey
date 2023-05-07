from datetime import datetime, timezone
from unittest import TestCase

from jsonschema import ValidationError
from jsonschema.validators import validator_for

from schemey import schema_from_json, schema_from_type
from schemey.json_schema.timestamp import timestamp


class TestRanges(TestCase):
    def test_past_no_grace_period(self):
        schema = schema_from_json(
            {"type": "string", "format": "date-time", "timestamp": {"past": True}}
        )
        schema.validate("2020-01-01")
        timestamp = (
            datetime.fromtimestamp(datetime.now().timestamp() + 10)
            .astimezone(timezone.utc)
            .isoformat()
        )
        with self.assertRaises(ValidationError):
            schema.validate(timestamp)

    def test_past_grace_period(self):
        schema = schema_from_json(
            {
                "type": "string",
                "format": "date-time",
                "timestamp": {"past": True, "gracePeriodSeconds": 20},
            }
        )
        schema.validate("2020-01-01")
        timestamp = (
            datetime.fromtimestamp(datetime.now().timestamp() + 10)
            .astimezone(timezone.utc)
            .isoformat()
        )
        schema.validate(timestamp)

    def test_future_no_grace_period(self):
        schema = schema_from_json(
            {"type": "string", "format": "date-time", "timestamp": {}}
        )
        timestamp = (
            datetime.fromtimestamp(datetime.now().timestamp() + 10)
            .astimezone(timezone.utc)
            .isoformat()
        )
        schema.validate(timestamp)
        timestamp = (
            datetime.fromtimestamp(datetime.now().timestamp() - 1)
            .astimezone(timezone.utc)
            .isoformat()
        )
        with self.assertRaises(ValidationError):
            schema.validate(timestamp)

    def test_future_grace_period(self):
        schema = schema_from_json(
            {
                "type": "string",
                "format": "date-time",
                "timestamp": {
                    "gracePeriodSeconds": 20,
                },
            }
        )
        timestamp = (
            datetime.fromtimestamp(datetime.now().timestamp() + 20)
            .astimezone(timezone.utc)
            .isoformat()
        )
        schema.validate(timestamp)
        timestamp = (
            datetime.fromtimestamp(datetime.now().timestamp() - 1)
            .astimezone(timezone.utc)
            .isoformat()
        )
        schema.validate(timestamp)

    def test_past_date_only(self):
        schema = schema_from_json(
            {"type": "string", "format": "date", "timestamp": {"past": True}}
        )
        schema.validate("2020-01-01")
        ts = (
            datetime.fromtimestamp(datetime.now().timestamp() + 10)
            .astimezone(timezone.utc)
            .replace(hour=23, minute=59, second=59)
            .strftime("%Y-%m-%d")
        )
        schema.validate(ts)
        ts = (
            datetime.fromtimestamp(datetime.now().timestamp() + 86401)
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%d")
        )
        with self.assertRaises(ValidationError):
            schema.validate(ts)

    def test_past_date_only_grace_period(self):
        schema = schema_from_json(
            {
                "type": "string",
                "format": "date",
                "timestamp": {"past": True, "gracePeriodSeconds": 86400},
            }
        )
        ts = (
            datetime.fromtimestamp(datetime.now().timestamp() + 86401)
            .astimezone(timezone.utc)
            .replace(hour=23, minute=59, second=59)
            .strftime("%Y-%m-%d")
        )
        schema.validate(ts)
        ts = (
            datetime.fromtimestamp(datetime.now().timestamp() + 24 * 60 * 60 * 2)
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%d")
        )
        with self.assertRaises(ValidationError):
            schema.validate(ts)

    def test_non_date(self):
        schema = schema_from_type(str)
        schema.validate("2020-01-01")
        schema.schema["timestamp"] = {}
        self.assertTrue(list(schema.iter_errors("2020-01-01")))
