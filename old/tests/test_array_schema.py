from typing import List, Tuple, Set
from unittest import TestCase

from schemey import ArraySchema
from schemey import NumberSchema
from schemey import schema_for_type
from schemey import SchemaError
from schemey import StringSchema


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
        errors = list(schema.get_schema_errors([1, 2, 3], ['foobar']))
        assert errors == [SchemaError('foobar', 'max_items', [1, 2, 3])]

    def test_to_json_schema(self):
        dumped = ArraySchema[float](NumberSchema(item_type=float)).dump_json_schema()
        assert dumped == dict(type='array', items=dict(type='number'))
        json_schema = dict(type='array', items=dict(type='string'), minItems=5, maxItems=10, uniqueness=True)
        schema = ArraySchema(item_schema=StringSchema(), min_items=5, max_items=10, uniqueness=True)
        dumped = schema.dump_json_schema()
        assert dumped == json_schema

    def test_item_type(self):
        item_type = List[str]
        schema = schema_for_type(item_type)
        assert schema.item_type == item_type
        assert list(schema.get_schema_errors(('foo', 'bar')))
        assert list(schema.get_schema_errors(['foo', 1]))
        assert not list(schema.get_schema_errors(['foo', 'bar']))
        assert list(schema.get_schema_errors({'foo', 'bar'}))

    def test_tuple(self):
        item_type = Tuple[str, ...]
        schema = schema_for_type(item_type)
        assert schema.item_type == item_type
        assert not list(schema.get_schema_errors(('foo', 'bar')))
        assert list(schema.get_schema_errors(('foo', 1)))
        assert list(schema.get_schema_errors(['foo', 'bar']))
        assert list(schema.get_schema_errors({'foo', 'bar'}))

    def test_set(self):
        item_type = Set[str]
        schema = schema_for_type(item_type)
        assert schema.item_type == item_type
        assert list(schema.get_schema_errors(('foo', 'bar')))
        assert list(schema.get_schema_errors({'foo', 1}))
        assert list(schema.get_schema_errors(['foo', 'bar']))
        assert not list(schema.get_schema_errors({'foo', 'bar'}))

    def test_no_item_type(self):
        schema = ArraySchema(item_schema=StringSchema())
        assert schema.item_type == List[str]
