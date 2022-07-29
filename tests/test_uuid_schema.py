from unittest import TestCase
from uuid import UUID, uuid4

from jsonschema import ValidationError
from marshy import dump, load

from schemey import schema_from_type, Schema, get_default_schema_context


class TestUuidSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(UUID)
        expected = Schema({"type": "string", "format": "uuid"}, UUID)
        self.assertEqual(expected, schema)

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.schema_from_type(UUID)
        schema.validate(str(uuid4()))
        with self.assertRaises(ValidationError):
            schema.validate("Foobar")

    def test_dump_and_load(self):
        schema = schema_from_type(UUID)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)
