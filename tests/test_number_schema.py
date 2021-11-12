from unittest import TestCase

from schemey.number_schema import NumberSchema
from schemey.schema_error import SchemaError


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

    def test_to_json_schema(self):
        assert dict(type='integer') == NumberSchema(item_type=int).to_json_schema()
        assert dict(type='number') == NumberSchema(item_type=float).to_json_schema()
        json_schema = dict(type='integer', minimum=5, maximum=10, exclusiveMinimum=True, exclusiveMaximum=False)
        schema = NumberSchema(int, minimum=5, maximum=10, exclusive_minimum=True, exclusive_maximum=False)
        assert schema.to_json_schema() == json_schema
