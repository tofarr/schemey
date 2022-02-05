from typing import Tuple
from unittest import TestCase

from marshy import dump

from schemey.factory.tuple_schema_factory import TupleSchemaFactory
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC
from schemey.schemey_context import schema_for_type


class TestTupleSchema(TestCase):

    def test_create_tuple_schema(self):
        my_tuple = Tuple[int, str, bool]
        schema = schema_for_type(my_tuple).json_schema
        dumped = dump(schema, SchemaABC)
        expected = {
            'items': False,
            'prefixItems': [{'type': 'integer'}, {'type': 'string'}, {'type': 'boolean'}],
            'type': 'array'
        }
        self.assertEqual(expected, dumped)

    def test_factory_ellipsis(self):
        type_ = Tuple[int, ...]
        json_schema_context = JsonSchemaContext()
        self.assertIsNone(TupleSchemaFactory().create(type_, json_schema_context))