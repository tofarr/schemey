from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

from schemey import get_default_schema_context, Schema, schema_from_type


class TestBooleanSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(bool)
        expected = Schema({"type": "boolean"}, bool)
        self.assertEqual(expected, schema)

    def test_iter_errors(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(bool)
        self.assertEqual([], list(schema.iter_errors(True)))
        self.assertEqual([], list(schema.iter_errors(False)))
        self.assertEqual(1, len(list(schema.iter_errors("True"))))

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(bool)
        with self.assertRaises(ValidationError):
            schema.validate(10)

    def test_dump_and_load(self):
        schema = schema_from_type(bool)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)
