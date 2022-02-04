from unittest import TestCase

from marshy import load, dump

from schemey.boolean_schema import BooleanSchema
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.schema import Schema
from schemey.schemey_context import get_default_schemey_context


class TestBooleanSchema(TestCase):

    def test_factory_no_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        expected = Schema(
            BooleanSchema(default=NoDefault),
            context.marshaller_context.get_marshaller(bool)
        )
        self.assertEqual(expected, schema)

    def test_factory_with_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool, True)
        expected = BooleanSchema(default=True)
        self.assertEqual(expected, schema.json_schema)

    def test_get_schema_errors(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        # Boolean schema actaully accepts anything and converts it to truthy / falsy
        self.assertEqual(list(schema.get_schema_errors(True)), [])
        self.assertEqual(list(schema.get_schema_errors(False)), [])
        self.assertEqual(list(schema.get_schema_errors('True')), [])
        self.assertEqual(list(schema.get_schema_errors('0')), [])
        self.assertEqual(list(schema.get_schema_errors({})), [])

    def test_validate(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        schema.validate(10)

    def test_dump_and_load(self):
        schema = BooleanSchema()
        dumped = dump(schema)
        loaded = load(JsonSchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_default(self):
        schema = BooleanSchema(default=True)
        dumped = dump(schema)
        expected_dump = dict(type='boolean', default=True)
        self.assertEqual(expected_dump, dumped)
        loaded = load(JsonSchemaABC, dumped)
        self.assertEqual(schema, loaded)
