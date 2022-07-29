from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

from schemey import schema_from_type, Schema, get_default_schema_context
from schemey.schema import int_schema


class TestIntegerSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(int)
        expected = Schema({"type": "integer"}, int)
        self.assertEqual(expected, schema)

    def test_iter_errors(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(int)
        self.assertEqual([], list(schema.iter_errors(10)))
        self.assertEqual([], list(schema.iter_errors(-1)))
        self.assertEqual(1, len(list(schema.iter_errors("True"))))

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(int)
        with self.assertRaises(ValidationError):
            schema.validate("Foobar")

    def test_dump_and_load(self):
        schema = schema_from_type(int)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)

    def test_minimum(self):
        schema = Schema(
            schema={"type": "integer", "minimum": 5},
            python_type=int,
        )
        schema.validate(6)
        schema.validate(5)
        with self.assertRaises(ValidationError):
            schema.validate(4)

    def test_maximum(self):
        schema = Schema(
            schema={"type": "integer", "maximum": 5},
            python_type=int,
        )
        schema.validate(4)
        schema.validate(5)
        with self.assertRaises(ValidationError):
            schema.validate(6)

    def test_exclusive_minimum(self):
        schema = Schema(
            schema={"type": "integer", "exclusiveMinimum": 5},
            python_type=int,
        )
        schema.validate(6)
        with self.assertRaises(ValidationError):
            schema.validate(5)
        with self.assertRaises(ValidationError):
            schema.validate(4)

    def test_exclusive_maximum(self):
        schema = Schema(
            schema={"type": "integer", "exclusiveMaximum": 5},
            python_type=int,
        )
        schema.validate(4)
        with self.assertRaises(ValidationError):
            schema.validate(5)
        with self.assertRaises(ValidationError):
            schema.validate(6)

    def test_int_schema(self):
        schema = int_schema(
            minimum=2, maximum=6, exclusive_minimum=1, exclusive_maximum=7
        )
        expected = Schema(
            {
                "type": "integer",
                "minimum": 2,
                "maximum": 6,
                "exclusiveMinimum": 1,
                "exclusiveMaximum": 7,
            },
            int,
        )
        self.assertEqual(expected, schema)
