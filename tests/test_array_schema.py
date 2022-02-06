from unittest import TestCase

from marshy import dump

from schemey.array_schema import ArraySchema
from schemey.integer_schema import IntegerSchema
from schemey.number_schema import NumberSchema
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema


# noinspection PyTypeChecker
class TestArraySchema(TestCase):

    def test_schema_string_array(self):
        schema = ArraySchema(item_schema=StringSchema())
        assert list(schema.get_schema_errors(['a', 'b', 'c'])) == []
        assert list(schema.get_schema_errors('foo')) == [SchemaError('', 'type', 'foo')]
        assert list(schema.get_schema_errors([10])) == [SchemaError('0', 'type', 10)]

    def test_schema_unique_int_array(self):
        schema = ArraySchema(item_schema=IntegerSchema(), uniqueness=True)
        assert list(schema.get_schema_errors([1, 2, 3])) == []
        assert list(schema.get_schema_errors([1, 2, 2])) == [SchemaError('2', 'non_unique', 2)]
        assert list(schema.get_schema_errors([])) == []

    def test_schema_min_items(self):
        schema = ArraySchema(item_schema=IntegerSchema(), min_items=2)
        assert list(schema.get_schema_errors([1, 2, 3])) == []
        assert list(schema.get_schema_errors([1, 2])) == []
        assert list(schema.get_schema_errors([1], ['foobar'])) == [SchemaError('foobar', 'min_items', [1])]

    def test_schema_max_items(self):
        schema = ArraySchema(item_schema=IntegerSchema(), max_items=2)
        assert list(schema.get_schema_errors([1])) == []
        assert list(schema.get_schema_errors([1, 2])) == [SchemaError('', 'max_items', [1, 2])]
        errors = list(schema.get_schema_errors([1, 2, 3], ['foobar']))
        assert errors == [SchemaError('foobar', 'max_items', [1, 2, 3])]

    def test_dump_and_load(self):
        dumped = dump(ArraySchema(NumberSchema()))
        assert dumped == dict(type='array', items=dict(type='number'))
        json_schema = dict(type='array', items=dict(type='string'), minItems=5, maxItems=10, uniqueness=True)
        schema = ArraySchema(item_schema=StringSchema(), min_items=5, max_items=10, uniqueness=True)
        dumped = dump(schema)
        assert dumped == json_schema
