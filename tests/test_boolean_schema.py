from unittest import TestCase

from marshy import load, dump

from schemey.boolean_schema import BooleanSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context


class TestBooleanSchema(TestCase):

    def test_factory(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        expected = BooleanSchema()
        self.assertEqual(expected, schema)

    def test_get_schema_errors(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        # Boolean schema actaully accepts anything and converts it to truthy / falsy
        self.assertEqual([], list(schema.get_schema_errors(True)))
        self.assertEqual([], list(schema.get_schema_errors(False)))
        self.assertEqual([SchemaError('', 'type', 'True')], list(schema.get_schema_errors('True')))
        self.assertEqual([SchemaError('a/b', 'type', 'True')], list(schema.get_schema_errors('True', ['a', 'b'])))

    def test_validate(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        with self.assertRaises(SchemaError):
            schema.validate(10)

    def test_dump_and_load(self):
        schema = BooleanSchema()
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)
