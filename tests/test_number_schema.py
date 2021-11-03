from unittest import TestCase

from marshy.default_context import new_default_context

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.number_schema import NumberSchema
from persisty.schema.schema_error import SchemaError


class TestNumberSchema(TestCase):

    def test_schema_int(self):
        schema = NumberSchema(item_type=int)
        assert list(schema.get_schema_errors(10)) == []
        assert list(schema.get_schema_errors(10.2)) == [SchemaError('', 'type', 10.2)]
        assert list(schema.get_schema_errors(10.2, [])) == [SchemaError('', 'type', 10.2)]
        assert list(schema.get_schema_errors(10.2, ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 10.2)]

    def test_schema_float(self):
        schema = NumberSchema(item_type=float)
        assert list(schema.get_schema_errors(10)) == []
        assert list(schema.get_schema_errors(10.2)) == []
        assert list(schema.get_schema_errors(10.2, [])) == []
        assert list(schema.get_schema_errors(10.2, [])) == []
        assert list(schema.get_schema_errors(10, [])) == []
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('10', ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', '10')]

    def test_schema_minimum(self):
        schema = NumberSchema(item_type=int, minimum=10)
        assert list(schema.get_schema_errors(11)) == []
        assert list(schema.get_schema_errors(10)) == []
        assert list(schema.get_schema_errors(9, ['foobar'])) == [SchemaError('foobar', 'minimum', 9)]

    def test_schema_minimum_exclusive(self):
        schema = NumberSchema(item_type=int, minimum=10, exclusive_minimum=True)
        assert list(schema.get_schema_errors(11)) == []
        assert list(schema.get_schema_errors(10)) == [SchemaError('', 'exclusive_minimum', 10)]
        assert list(schema.get_schema_errors(9, ['foobar'])) == [SchemaError('foobar', 'minimum', 9)]

    def test_schema_maximum(self):
        schema = NumberSchema(item_type=int, maximum=10)
        assert list(schema.get_schema_errors(9)) == []
        assert list(schema.get_schema_errors(10)) == [SchemaError('', 'exclusive_maximum', 10)]
        assert list(schema.get_schema_errors(11, ['foobar'])) == [SchemaError('foobar', 'maximum', 11)]

    def test_schema_maximum_exclusive(self):
        schema = NumberSchema(item_type=int, maximum=10, exclusive_maximum=False)
        assert list(schema.get_schema_errors(9)) == []
        assert list(schema.get_schema_errors(10)) == []
        assert list(schema.get_schema_errors(11, ['foobar'])) == [SchemaError('foobar', 'maximum', 11)]

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(NumberSchema, dict(type='integer')) == NumberSchema(item_type=int)
        assert context.load(NumberSchema, dict(type='number')) == NumberSchema(item_type=float)
        json_schema = dict(type='integer', minimum=5, maximum=10, exclusiveMinimum=True, exclusiveMaximum=False)
        schema = NumberSchema(int, minimum=5, maximum=10, exclusive_minimum=True, exclusive_maximum=False)
        assert context.load(SchemaABC, json_schema) == schema
        assert context.dump(schema) == json_schema
