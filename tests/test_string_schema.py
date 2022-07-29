from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

from schemey import schema_from_type, Schema, get_default_schema_context
from schemey.schema import str_schema


class TestFloatSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(str)
        expected = Schema({"type": "string"}, str)
        self.assertEqual(expected, schema)

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(str)
        schema.validate("foobar")
        with self.assertRaises(ValidationError):
            schema.validate(10)

    def test_dump_and_load(self):
        schema = schema_from_type(str)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)

    def test_min_length(self):
        schema = Schema(
            schema={"type": "string", "minLength": 5},
            python_type=str,
        )
        schema.validate("123456")
        schema.validate("12345")
        with self.assertRaises(ValidationError):
            schema.validate("1234")

    def test_max_length(self):
        schema = Schema(
            schema={"type": "string", "maxLength": 5},
            python_type=str,
        )
        schema.validate("1234")
        schema.validate("12345")
        with self.assertRaises(ValidationError):
            schema.validate("123456")

    def test_pattern(self):
        schema = Schema(
            schema={"type": "string", "pattern": "^\\w+$"},
            python_type=str,
        )
        schema.validate("foobar")
        schema.validate("foo_bar123")
        with self.assertRaises(ValidationError):
            schema.validate("foo!bar")

    def test_format_string(self):
        schema = str_schema(str_format="email")
        expected = Schema({"type": "string", "format": "email"}, str)
        self.assertEqual(expected, schema)
