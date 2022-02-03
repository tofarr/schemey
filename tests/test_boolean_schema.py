from unittest import TestCase

from schemey.boolean_schema import BooleanSchema
from schemey.json_schema_abc import NoDefault
from schemey.schema import Schema
from schemey.schemey_context import get_default_schemey_context


class TestBooleanSchema(TestCase):

    def test_factory_no_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool)
        expected = Schema(
            BooleanSchema(default_value=NoDefault),
            context.marshaller_context.get_marshaller(bool)
        )
        self.assertEqual(expected, schema)

    def test_factory_with_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(bool, True)
        expected = BooleanSchema(default_value=True)
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

    def test_load(self):
        context = get_default_schemey_context()
        self.assertEqual(context.load_json_schema(dict(type='boolean')), BooleanSchema())
        to_load = dict(type='boolean', default=True)
        loaded = context.load_json_schema(to_load)
        expected = BooleanSchema(default_value=True)
        self.assertEqual(loaded, expected)

    def test_dump(self):
        context = get_default_schemey_context()
        self.assertEqual(context.dump_json_schema(BooleanSchema()), dict(type='boolean'))
        to_dump = BooleanSchema(default_value=True)
        dumped = context.dump_json_schema(to_dump)
        expected = dict(type='boolean', default=True)
        self.assertEqual(dumped, expected)
