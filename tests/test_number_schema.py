from unittest import TestCase

from schemey.json_schema_abc import NoDefault
from schemey.number_schema import NumberSchema
from schemey.schema import Schema
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context


class TestNumberSchema(TestCase):

    def test_factory_no_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(float)
        expected = Schema(
            NumberSchema(default_value=NoDefault),
            context.marshaller_context.get_marshaller(float)
        )
        self.assertEqual(expected, schema)

    def test_factory_with_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(float, 10.5)
        expected = NumberSchema(default_value=10.5)
        self.assertEqual(expected, schema.json_schema)

    def test_get_schema_errors(self):
        context = get_default_schemey_context()
        schema = context.get_schema(float)
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(list(schema.get_schema_errors(10.5)), [])
        self.assertEqual(list(schema.get_schema_errors('foo', [])), [SchemaError('', 'type', 'foo')])
        self.assertEqual(list(schema.get_schema_errors(False, ['foo', 'bar'])), [SchemaError('foo/bar', 'type', False)])

    def test_validate(self):
        context = get_default_schemey_context()
        schema = context.get_schema(float)
        schema.validate(10)

    def test_validate_fail(self):
        context = get_default_schemey_context()
        schema = context.get_schema(float)
        with self.assertRaises(SchemaError):
            schema.validate(None)

    def test_schema_minimum(self):
        schema = NumberSchema(minimum=10)
        self.assertEqual(list(schema.get_schema_errors(11)), [])
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(list(schema.get_schema_errors(9, ['foobar'])), [SchemaError('foobar', 'minimum', 9)])

    def test_schema_minimum_exclusive(self):
        schema = NumberSchema(exclusive_minimum=10)
        self.assertEqual(list(schema.get_schema_errors(11)), [])
        self.assertEqual(list(schema.get_schema_errors(10)), [SchemaError('', 'exclusive_minimum', 10)])
        self.assertEqual(list(schema.get_schema_errors(9, ['foobar'])), [SchemaError('foobar', 'exclusive_minimum', 9)])

    def test_schema_maximum(self):
        schema = NumberSchema(maximum=10)
        self.assertEqual(list(schema.get_schema_errors(9)), [])
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(list(schema.get_schema_errors(11, ['foobar'])), [SchemaError('foobar', 'maximum', 11)])

    def test_schema_maximum_exclusive(self):
        schema = NumberSchema(exclusive_maximum=10)
        self.assertEqual(list(schema.get_schema_errors(9)), [])
        self.assertEqual(list(schema.get_schema_errors(10)), [SchemaError('', 'exclusive_maximum', 10)])
        self.assertEqual(list(schema.get_schema_errors(11, ['foo'])), [SchemaError('foo', 'exclusive_maximum', 11)])

    def test_load(self):
        context = get_default_schemey_context()
        self.assertEqual(context.load_json_schema(dict(type='number')), NumberSchema())
        to_load = dict(type='number', default=7, minimum=5, exclusiveMinimum=4, maximum=9, exclusiveMaximum=10)
        loaded = context.load_json_schema(to_load)
        expected = NumberSchema(default_value=7, minimum=5, exclusive_minimum=4, maximum=9, exclusive_maximum=10)
        self.assertEqual(loaded, expected)

    def test_load_fail(self):
        context = get_default_schemey_context()
        with self.assertRaises(StopIteration):
            context.load_json_schema({})

    def test_dump(self):
        context = get_default_schemey_context()
        self.assertEqual(context.dump_json_schema(NumberSchema()), dict(type='number'))
        to_dump = NumberSchema(default_value=7, minimum=5, exclusive_minimum=4, maximum=9, exclusive_maximum=10)
        dumped = context.dump_json_schema(to_dump)
        expected = dict(type='number', default=7, minimum=5, exclusiveMinimum=4, maximum=9, exclusiveMaximum=10)
        self.assertEqual(dumped, expected)
