from unittest import TestCase

from schemey.boolean_schema import BooleanSchema
from schemey.json_schema_abc import NoDefault
from schemey.null_schema import NullSchema
from schemey.schema import Schema
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context


class TestBooleanSchema(TestCase):

    def test_factory_no_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(type(None))
        expected = Schema(
            NullSchema(default_value=NoDefault),
            context.marshaller_context.get_marshaller(type(None))
        )
        self.assertEqual(expected, schema)

    def test_factory_with_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(type(None), None)
        expected = NullSchema(default_value=None)
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

    def test_load(self):
        context = get_default_schemey_context()
        self.assertEqual(context.load_json_schema(dict(type='null')), NullSchema())
        to_load = dict(type='null', default=None)
        loaded = context.load_json_schema(to_load)
        expected = NullSchema(default_value=None)
        self.assertEqual(loaded, expected)

    def test_dump(self):
        context = get_default_schemey_context()
        self.assertEqual(context.dump_json_schema(NullSchema()), dict(type='null'))
        to_dump = NullSchema(default_value=None)
        dumped = context.dump_json_schema(to_dump)
        expected = dict(type='null', default=None)
        self.assertEqual(dumped, expected)
