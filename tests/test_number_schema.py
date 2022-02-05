from unittest import TestCase

from marshy import dump, load

from schemey.schema_abc import SchemaABC
from schemey.number_schema import NumberSchema
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context


class TestNumberSchema(TestCase):

    def test_factory(self):
        context = get_default_schemey_context()
        schema = context.get_schema(float)
        expected = NumberSchema()
        self.assertEqual(expected, schema)

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

    def test_dump_and_load(self):
        schema = NumberSchema()
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_range(self):
        schema = NumberSchema(minimum=5, maximum=9)
        dumped = dump(schema)
        expected_dump = dict(type='number', minimum=5, maximum=9)
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_exclusive_range(self):
        schema = NumberSchema(exclusive_minimum=4,exclusive_maximum=10)
        dumped = dump(schema)
        expected_dump = dict(type='number', exclusiveMinimum=4, exclusiveMaximum=10)
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_load_fail(self):
        with self.assertRaises(ValueError):
            load(SchemaABC, {})

    def test_simplify(self):
        self.assertEqual(dict(type='number', exclusiveMinimum=5),
                          dump(NumberSchema(minimum=5, exclusive_minimum=5).simplify()))
        self.assertEqual(dict(type='number', exclusiveMinimum=5),
                          dump(NumberSchema(minimum=4, exclusive_minimum=5).simplify()))
        self.assertEqual(dict(type='number', minimum=6),
                          dump(NumberSchema(minimum=6, exclusive_minimum=5).simplify()))
        self.assertEqual(dict(type='number', exclusiveMaximum=5),
                          dump(NumberSchema(maximum=5, exclusive_maximum=5).simplify()))
        self.assertEqual(dict(type='number', exclusiveMaximum=5),
                          dump(NumberSchema(maximum=6, exclusive_maximum=5).simplify()))
        self.assertEqual(dict(type='number', maximum=4),
                          dump(NumberSchema(maximum=4, exclusive_maximum=5).simplify()))
