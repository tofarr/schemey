from typing import Union
from unittest import TestCase

from schemey.any_of_schema import AnyOfSchema, strip_optional, optional_schema
from schemey.boolean_schema import BooleanSchema
from schemey.graphql.graphql_attr import GraphqlAttr
from schemey.graphql.graphql_object_type import GraphqlObjectType
from schemey.graphql_context import GraphqlContext
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schema_context import schema_for_type
from schemey.schema_error import SchemaError
from schemey.string_format import StringFormat
from schemey.string_schema import StringSchema


class TestAnyOfSchema(TestCase):

    def test_optional_schema(self):
        schema = AnyOfSchema((NullSchema(), StringSchema()))
        assert list(schema.get_schema_errors('foo')) == []
        assert list(schema.get_schema_errors(None)) == []
        assert list(schema.get_schema_errors(10)) == [SchemaError('', 'type', 10)]
        assert list(schema.get_schema_errors(10, ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 10)]

    def test_to_json_schema(self):
        schema = AnyOfSchema((NumberSchema(item_type=int), NullSchema()), 10)
        json_schema = dict(anyOf=[dict(type='integer'), dict(type='null')], default=10)
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

    def test_to_graphql_union(self):
        schema = AnyOfSchema((NumberSchema(int), StringSchema()))
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema.to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = 'union AnyOfIntString = Int | String\n'  # I dunno if graphql impls will even let you do this...
        assert graphql == expected

    def test_to_graphql_optional(self):
        schema = optional_schema(StringSchema())
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema.to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = ''
        assert graphql == expected

    def test_to_graphql(self):
        schema = AnyOfSchema((NullSchema(), NullSchema()))
        assert schema.to_graphql_attr() is None
        # noinspection PyTypeChecker
        assert schema.to_graphql_schema(None) is None

    def test_to_graphql_attr_custom_name(self):
        schema = AnyOfSchema((StringSchema(format=StringFormat.EMAIL),
                              StringSchema(format=StringFormat.URI)),
                             name='EmailOrUri')
        assert schema.to_graphql_attr() == GraphqlAttr('EmailOrUri')
        json_schema = schema.to_json_schema()
        expected = {'anyOf': [{'type': 'string', 'format': 'email'}, {'type': 'string', 'format': 'uri'}]}
        assert expected == json_schema
