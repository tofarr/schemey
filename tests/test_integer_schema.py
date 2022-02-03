from unittest import TestCase

from schemey.integer_schema import IntegerSchema
from schemey.json_schema_abc import NoDefault
from schemey.number_schema import NumberSchema
from schemey.schema import Schema
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context


class TestIntegerSchema(TestCase):

    def test_factory_no_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(int)
        expected = Schema(
            IntegerSchema(default_value=NoDefault),
            context.marshaller_context.get_marshaller(int)
        )
        self.assertEqual(expected, schema)

    def test_factory_with_default(self):
        context = get_default_schemey_context()
        schema = context.get_schema(int, 10)
        expected = IntegerSchema(default_value=10)
        self.assertEqual(expected, schema.json_schema)

    def test_get_schema_errors(self):
        context = get_default_schemey_context()
        schema = context.get_schema(int)
        self.assertEqual(list(schema.get_schema_errors(10)), [])
        self.assertEqual(list(schema.get_schema_errors(10.2)), [SchemaError('', 'type', 10.2)])
        self.assertEqual(list(schema.get_schema_errors(10.2, [])), [SchemaError('', 'type', 10.2)])
        self.assertEqual(list(schema.get_schema_errors(10.2, ['foo', 'bar'])), [SchemaError('foo/bar', 'type', 10.2)])

    def test_validate(self):
        context = get_default_schemey_context()
        schema = context.get_schema(int)
        schema.validate(10)

    def test_validate_fail(self):
        context = get_default_schemey_context()
        schema = context.get_schema(int)
        with self.assertRaises(SchemaError):
            schema.validate(10.5)

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
        self.assertEqual(context.load_json_schema(dict(type='integer')), IntegerSchema())
        to_load = dict(type='integer', default=7, minimum=5, exclusiveMinimum=4, maximum=9, exclusiveMaximum=10)
        loaded = context.load_json_schema(to_load)
        expected = IntegerSchema(default_value=7, minimum=5, exclusive_minimum=4, maximum=9, exclusive_maximum=10)
        self.assertEqual(loaded, expected)

    def test_load_fail(self):
        context = get_default_schemey_context()
        with self.assertRaises(StopIteration):
            context.load_json_schema({})

    def test_dump(self):
        context = get_default_schemey_context()
        self.assertEqual(context.dump_json_schema(IntegerSchema()), dict(type='integer'))
        to_dump = IntegerSchema(default_value=7, minimum=5, exclusive_minimum=4, maximum=9, exclusive_maximum=10)
        dumped = context.dump_json_schema(to_dump)
        expected = dict(type='integer', default=7, minimum=5, exclusiveMinimum=4, maximum=9, exclusiveMaximum=10)
        self.assertEqual(dumped, expected)
