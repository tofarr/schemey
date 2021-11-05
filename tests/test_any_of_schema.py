from unittest import TestCase

from marshy import dump, load
from marshy.default_context import new_default_context

from persisty.schema.any_of_schema import AnyOfSchema
from persisty.schema.boolean_schema import BooleanSchema
from persisty.schema.null_schema import NullSchema
from persisty.schema.number_schema import NumberSchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError
from persisty.schema.string_schema import StringSchema


class TestAnyOfSchema(TestCase):

    def test_optional_schema(self):
        schema = AnyOfSchema((NullSchema(), StringSchema()))
        assert list(schema.get_schema_errors('foo')) == []
        assert list(schema.get_schema_errors(None)) == []
        assert list(schema.get_schema_errors(10)) == [SchemaError('', 'type', 10)]
        assert list(schema.get_schema_errors(10, ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 10)]

    def test_marshalling(self):
        context = new_default_context()
        schema = AnyOfSchema((NumberSchema(item_type=int), NullSchema()))
        json_schema = dict(type=['integer', None])
        assert context.load(AnyOfSchema, json_schema) == schema
        assert context.dump(schema) == json_schema

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
        expected = AnyOfSchema((
            NumberSchema(int),
            StringSchema(),
            BooleanSchema()
        ))
        assert loaded == expected
