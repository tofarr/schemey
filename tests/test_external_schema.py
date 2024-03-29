from unittest import TestCase
from uuid import uuid4

from jsonschema import ValidationError
from marshy import load, dump
from marshy.types import ExternalItemType, ExternalType

from schemey import schema_from_type, Schema


class TestEnumSchema(TestCase):
    def test_item_factory(self):
        schema = schema_from_type(ExternalItemType)
        expected = Schema(
            {"type": "object", "additionalProperties": True}, ExternalItemType
        )
        self.assertEqual(expected, schema)

    def test_factory(self):
        schema = schema_from_type(ExternalType)
        expected = Schema({}, ExternalType)
        self.assertEqual(expected, schema)

    def test_item_dump_and_load(self):
        schema = schema_from_type(ExternalItemType)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(loaded, schema)

    def test_dump_and_load(self):
        schema = schema_from_type(ExternalType)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(loaded, schema)

    def test_item_validate(self):
        schema = schema_from_type(ExternalItemType)
        schema.validate({"foo": "bar", "zap": [1, 2.5, True]})
        with self.assertRaises(ValidationError):
            schema.validate([])
        with self.assertRaises(ValidationError):
            schema.validate(uuid4())

    def test_validate(self):
        schema = schema_from_type(ExternalType)
        schema.validate({"foo": "bar", "zap": [1, 2.5, True]})
        schema.validate([])
