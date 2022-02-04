from unittest import TestCase

from marshy import dump, load

from schemey.boolean_schema import BooleanSchema
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.null_schema import NullSchema
from schemey.schema import Schema
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context


class TestBooleanSchema(TestCase):

    def test_factory_no_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(type(None))
        expected = Schema(
            NullSchema(default=NoDefault),
            context.marshaller_context.get_marshaller(type(None))
        )
        self.assertEqual(expected, schema)

    def test_factory_with_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(type(None), None)
        expected = NullSchema(default=None)
        self.assertEqual(expected, schema.json_schema)

    def test_null_schema(self):
        schema = NullSchema()
        errors = list(schema.get_schema_errors('True', ['foo', 'bar']))
        # noinspection PyTypeChecker
        self.assertEqual(errors, [SchemaError('foo/bar', 'type', 'True')])
        self.assertEqual(list(schema.get_schema_errors(None)), [])

    def test_validate(self):
        context = get_default_schemey_context()
        schema = context.get_schema(type(None))
        schema.validate(None)

    def test_validate_fail(self):
        context = get_default_schemey_context()
        schema = context.get_schema(type(None))
        with self.assertRaises(SchemaError):
            schema.validate('Not None!')

    def test_dump_and_load(self):
        schema = NullSchema()
        dumped = dump(schema)
        loaded = load(JsonSchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_default(self):
        schema = NullSchema(default=None)
        dumped = dump(schema)
        expected_dump = dict(type='null', default=None)
        self.assertEqual(expected_dump, dumped)
        loaded = load(JsonSchemaABC, dumped)
        self.assertEqual(schema, loaded)
