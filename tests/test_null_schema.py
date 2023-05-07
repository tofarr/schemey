from typing import Optional
from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

from schemey import schema_from_type, Schema, get_default_schema_context
from schemey.schema import optional_schema, str_schema


class TestNullSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(type(None))
        expected = Schema({"type": "null"}, type(None))
        self.assertEqual(expected, schema)

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(type(None))
        schema.validate(None)
        with self.assertRaises(ValidationError):
            schema.validate("Foobar")

    def test_dump_and_load(self):
        schema = schema_from_type(type(None))
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)

    def test_optional(self):
        schema = optional_schema(str_schema())
        expected = Schema(
            {"anyOf": [{"type": "null"}, {"type": "string"}]}, Optional[str]
        )
        self.assertEqual(schema, expected)
