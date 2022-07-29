from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

from schemey import schema_from_type, Schema, get_default_schema_context
from schemey.schema import float_schema


class TestFloatSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(float)
        expected = Schema({"type": "number"}, float)
        self.assertEqual(expected, schema)

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(float)
        with self.assertRaises(ValidationError):
            schema.validate("Foobar")

    def test_dump_and_load(self):
        schema = schema_from_type(float)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)

    def test_minimum(self):
        schema = Schema(
            schema={"type": "number", "minimum": 5.0},
            python_type=float,
        )
        schema.validate(6.0)
        schema.validate(5.0)
        with self.assertRaises(ValidationError):
            schema.validate(4.0)

    def test_maximum(self):
        schema = Schema(
            schema={"type": "number", "maximum": 5.0},
            python_type=float,
        )
        schema.validate(4.0)
        schema.validate(5.0)
        with self.assertRaises(ValidationError):
            schema.validate(6.0)

    def test_float_schema(self):
        schema = float_schema(
            minimum=2.0, maximum=6.0, exclusive_minimum=1.0, exclusive_maximum=7.0
        )
        expected = Schema(
            {
                "type": "number",
                "minimum": 2.0,
                "maximum": 6.0,
                "exclusiveMinimum": 1.0,
                "exclusiveMaximum": 7.0,
            },
            float,
        )
        self.assertEqual(expected, schema)
