from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from unittest import TestCase

from schemey.any_of_schema import optional_schema
from schemey.array_schema import ArraySchema
from schemey.deferred_schema import DeferredSchema
from schemey.graphql.graphql_object_type import GraphqlObjectType
from schemey.graphql_context import GraphqlContext
from schemey.number_schema import NumberSchema
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import schema_for_type, get_default_schema_context
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema
from tests.fixtures import Band, Node, Transaction, Issue


class TestObjectSchema(TestCase):

    def test_object_schema(self):
        schema = ObjectSchema(Band, [
            PropertySchema('id', StringSchema(min_length=1)),
            PropertySchema('band_name', optional_schema(StringSchema())),
            PropertySchema('year_formed', optional_schema(NumberSchema(int, minimum=1900))),
        ])
        assert list(schema.get_schema_errors(Band())) == [SchemaError('id', 'type')]
        assert list(schema.get_schema_errors(Band(''))) == [SchemaError('id', 'min_length', '')]
        assert list(schema.get_schema_errors(Band('mozart', 'Mozart', 1756))) == \
               [SchemaError('year_formed', 'minimum', 1756)]

    def test_to_json_schema(self):
        expected_json_schema = {
            "type": "object",
            "properties": {
                "some_str": {"type": "string"},
                "some_bool": {"type": "boolean"}
            },
            "additionalProperties": False
        }

        @dataclass
        class Foobar:
            some_str: str
            some_bool: bool

        schema = schema_for_type(Foobar)
        json_schema = schema.to_json_schema()
        assert expected_json_schema == json_schema

    def test_default(self):
        schema = ObjectSchema(Node, (
            PropertySchema('id', StringSchema()),
            PropertySchema('children', ArraySchema(DeferredSchema(get_default_schema_context(), Node))),
        ), Node('parent', None, [Node('child')]))
        json_schema = schema.to_json_schema()
        expected = {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'children': {'type': 'array', 'items': {'$ref': '#$defs/Node'}}
            },
            'additionalProperties': False,
            'default': {
                'id': 'parent',
                'parent': None,
                'children': [
                    {'id': 'child', 'parent': None, 'children': []}
                ]
            }
         }
        assert expected == json_schema

    def test_dict(self):
        schema = ObjectSchema(dict, [
            PropertySchema('foo', NumberSchema(int)),
            PropertySchema('bar', optional_schema(StringSchema()))
        ])
        schema.validate(dict(foo=1, bar='b'))
        schema.validate(dict(foo=1))
        with self.assertRaises(SchemaError):
            schema.validate(dict(foo=1, bar=2))
        with self.assertRaises(SchemaError):
            schema.validate(dict(foo=1, bar='b', zap='c'))

    def test_to_graphql(self):
        schema = schema_for_type(Band)
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema.to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = 'input Band {\n\tid: String\n\tband_name: String\n\tyear_formed: Int\n}\n\n'
        assert graphql == expected

    def test_to_graphql_dict(self):
        schema = ObjectSchema(dict, [
            PropertySchema('foo', NumberSchema(int)),
            PropertySchema('bar', optional_schema(StringSchema()))
        ], name='FooBar')
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema.to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = 'input FooBar {\n\tfoo: Int!\n\tbar: String\n}\n\n'
        assert graphql == expected

    def test_to_graphql_custom_doc_string(self):
        @dataclass
        class FooBar:
            """ A Bar of the Foo variety! """
            foo: int
            bar: List[str] = field(default_factory=list)
        schema = schema_for_type(FooBar)
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema.to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = '"""\nA Bar of the Foo variety!\n"""\ninput FooBar {\n\tfoo: Int!\n\tbar: [String!]!\n}\n\n'
        assert graphql == expected

    def test_nested(self):
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema_for_type(Node).to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        expected = 'input Node {\n\tid: String!\n\tparent: Node\n\tchildren: [Node!]!\n}\n\n'
        assert graphql == expected

    def test_multi(self):
        graphql_context = GraphqlContext(GraphqlObjectType.INPUT)
        schema_for_type(Transaction).to_graphql_schema(graphql_context)
        schema_for_type(Issue).to_graphql_schema(graphql_context)
        graphql = graphql_context.to_graphql()
        with open((Path(__file__).parent / 'multi_graphql.schema'), 'r') as f:
            expected = f.read()
        assert graphql == expected

    def test_to_graphql_no_attrs(self):
        @dataclass
        class NoAttrs:
            pass

        @dataclass
        class NoAttrsNested:
            no_attrs: NoAttrs

        schema: SchemaABC = schema_for_type(NoAttrsNested)
        context = GraphqlContext(GraphqlObjectType.TYPE)
        schema.to_graphql_schema(context)
        graphql = context.to_graphql()
        expected = ''
        assert expected == graphql
