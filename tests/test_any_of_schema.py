from unittest import TestCase

from marshy import dump, load
from marshy.default_context import new_default_context

from schema.any_of_schema import AnyOfSchema, strip_optional
from schema.boolean_schema import BooleanSchema
from schema.null_schema import NullSchema
from schema.number_schema import NumberSchema
from schema.schema_abc import SchemaABC
from schema.schema_error import SchemaError
from schema.string_schema import StringSchema


class TestAnyOfSchema(TestCase):

    def test_optional_schema(self):
        schema = AnyOfSchema((NullSchema(), StringSchema()))
        assert list(schema.get_schema_errors('foo', {})) == []
        assert list(schema.get_schema_errors(None, {})) == []
        assert list(schema.get_schema_errors(10, {})) == [SchemaError('', 'type', 10)]
        assert list(schema.get_schema_errors(10, {}, ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 10)]

    def test_marshalling(self):
        context = new_default_context()
        schema = AnyOfSchema((NumberSchema(item_type=int), NullSchema()))
        json_schema = dict(anyOf=[dict(type='integer'), dict(type=None)])
        loaded = context.load(AnyOfSchema, json_schema)
        dumped = context.dump(schema)
        assert loaded == schema
        assert dumped == json_schema

    def test_marshalling_nested(self):
        schema = AnyOfSchema((
            NumberSchema(int),
            AnyOfSchema((
                StringSchema(),
                BooleanSchema()
            ))
        ))
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        assert loaded == schema

    def test_strip_optional(self):
        assert strip_optional(StringSchema()) == StringSchema()
        assert strip_optional(AnyOfSchema(tuple((NullSchema(), StringSchema())))) == StringSchema()
        assert strip_optional(AnyOfSchema(tuple((StringSchema(), NullSchema())))) == StringSchema()
        schema = AnyOfSchema(tuple((StringSchema(), NumberSchema(int), NullSchema())))
        assert strip_optional(schema) is schema
        schema = AnyOfSchema(tuple((StringSchema(), NumberSchema(int))))
        assert strip_optional(schema) == schema
