from typing import Union
from unittest import TestCase

from schemey.any_of_schema import AnyOfSchema, strip_optional
from schemey.boolean_schema import BooleanSchema
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schema_context import schema_for_type
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema


class TestAnyOfSchema(TestCase):

    def test_optional_schema(self):
        schema = AnyOfSchema((NullSchema(), StringSchema()))
        assert list(schema.get_schema_errors('foo')) == []
        assert list(schema.get_schema_errors(None)) == []
        assert list(schema.get_schema_errors(10)) == [SchemaError('', 'type', 10)]
        assert list(schema.get_schema_errors(10, ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 10)]

    def test_to_json_schema(self):
        schema = AnyOfSchema((NumberSchema(item_type=int), NullSchema()))
        json_schema = dict(anyOf=[dict(type='integer'), dict(type='null')])
        dumped = schema.to_json_schema()
        assert dumped == json_schema

    def test_to_json_schema_flattened(self):
        schema = AnyOfSchema((
            NumberSchema(int),
            AnyOfSchema((
                StringSchema(),
                BooleanSchema()
            ))
        ))
        dumped = schema.to_json_schema()
        expected = {'anyOf': [{'type': 'integer'}, {'type': 'string'}, {'type': 'boolean'}]}
        assert expected == dumped

    def test_strip_optional(self):
        assert strip_optional(StringSchema()) == StringSchema()
        assert strip_optional(AnyOfSchema(tuple((NullSchema(), StringSchema())))) == StringSchema()
        assert strip_optional(AnyOfSchema(tuple((StringSchema(), NullSchema())))) == StringSchema()
        schema = AnyOfSchema(tuple((StringSchema(), NumberSchema(int), NullSchema())))
        assert strip_optional(schema) is schema
        schema = AnyOfSchema(tuple((StringSchema(), NumberSchema(int))))
        assert strip_optional(schema) == schema

    def test_item_type(self):
        item_type = Union[str, int, type(None)]
        schema = schema_for_type(item_type)
        assert schema.item_type == item_type

