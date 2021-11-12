from dataclasses import dataclass
from unittest import TestCase

from schemey.any_of_schema import optional_schema
from schemey.array_schema import ArraySchema
from schemey.deferred_schema import DeferredSchema
from schemey.number_schema import NumberSchema
from schemey.object_schema import ObjectSchema
from schemey.property_schema import PropertySchema
from schemey.schema_context import schema_for_type, get_default_schema_context
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema
from tests.fixtures import Band, Node


class TestObjectSchema(TestCase):

    def test_object_schema(self):
        schema = ObjectSchema(Band, [
            PropertySchema('id', StringSchema(min_length=1)),
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
