from unittest import TestCase

from marshy.default_context import new_default_context

from persisty.schema.array_schema import ArraySchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.number_schema import NumberSchema
from persisty.schema.schema_error import SchemaError
from persisty.schema.string_schema import StringSchema


class TestArraySchema(TestCase):

    def test_schema_string_array(self):
        schema = ArraySchema[str](item_schema=StringSchema())
        assert list(schema.get_schema_errors(['a', 'b', 'c'])) == []
        assert list(schema.get_schema_errors('foo')) == [SchemaError('', 'type', 'foo')]
        assert list(schema.get_schema_errors([10])) == [SchemaError('0', 'type', 10)]

    def test_schema_unique_int_array(self):
        schema = ArraySchema[int](item_schema=NumberSchema(item_type=int), uniqueness=True)
        assert list(schema.get_schema_errors([1, 2, 3])) == []
        assert list(schema.get_schema_errors([1, 2, 2])) == [SchemaError('2', 'non_unique', 2)]
        assert list(schema.get_schema_errors([])) == []

    def test_schema_min_items(self):
        schema = ArraySchema[int](item_schema=NumberSchema(item_type=int), min_items=2)
        assert list(schema.get_schema_errors([1, 2, 3])) == []
        assert list(schema.get_schema_errors([1, 2])) == []
        assert list(schema.get_schema_errors([1], ['foobar'])) == [SchemaError('foobar', 'min_items', [1])]

    def test_schema_max_items(self):
        schema = ArraySchema[int](item_schema=NumberSchema(item_type=int), max_items=2)
        assert list(schema.get_schema_errors([1])) == []
        assert list(schema.get_schema_errors([1, 2])) == [SchemaError('', 'max_items', [1, 2])]
        assert list(schema.get_schema_errors([1, 2, 3], ['foobar'])) == [SchemaError('foobar', 'max_items', [1, 2, 3])]

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(ArraySchema, dict(type='integer')) == NumberSchema(item_type=int)
        dumped = context.dump(ArraySchema[float](NumberSchema(item_type=float)))
        assert dumped == dict(type='array', items=dict(type='number'))
        json_schema = dict(type='array', items=dict(type='string'), minItems=5, maxItems=10, uniqueness=True)
        schema = ArraySchema(item_schema=StringSchema(), min_items=5, max_items=10, uniqueness=True)
        assert context.load(SchemaABC, json_schema) == schema
        assert context.dump(schema) == json_schema
