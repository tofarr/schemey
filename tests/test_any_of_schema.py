from typing import Union
from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

from schemey import get_default_schema_context, Schema, schema_from_type


class TestAnyOfSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(Union[bool, str])
        expected = Schema(
            {"anyOf": [{"type": "boolean"}, {"type": "string"}]}, Union[bool, str]
        )
        self.assertEqual(expected, schema)

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(Union[bool, str])
        schema.validate(True)
        schema.validate(False)
        schema.validate("A string")
        with self.assertRaises(ValidationError):
            schema.validate({})

    def test_dump_and_load(self):
        schema = schema_from_type(Union[bool, str])
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)
