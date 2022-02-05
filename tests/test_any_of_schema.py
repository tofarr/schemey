from typing import Union
from unittest import TestCase

from marshy import load, dump

from schemey.any_of_schema import AnyOfSchema
from schemey.boolean_schema import BooleanSchema
from schemey.const_schema import ConstSchema
from schemey.integer_schema import IntegerSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError
from schemey.schemey_context import get_default_schemey_context, schema_for_type
from schemey.string_schema import StringSchema
from schemey.tuple_schema import TupleSchema


class TestAnyOfSchema(TestCase):

    def test_factory(self):
        context = get_default_schemey_context()
        schema = context.get_schema(Union[bool, str])
        expected = AnyOfSchema(schemas=(
            TupleSchema((ConstSchema('bool'), BooleanSchema())),
            TupleSchema((ConstSchema('str'), StringSchema()))
        ))
        self.assertEqual(expected, schema)

    def test_get_schema_errors(self):
        context = get_default_schemey_context()
        schema = context.get_schema(Union[bool, str])
        # Boolean schema actaully accepts anything and converts it to truthy / falsy
        self.assertEqual([], list(schema.get_schema_errors(['bool', True])))
        self.assertEqual([], list(schema.get_schema_errors(['bool', False])))
        self.assertEqual([], list(schema.get_schema_errors(['str', 'True'])))
        self.assertEqual([], list(schema.get_schema_errors(['str', 'Yo'])))
        self.assertEqual([SchemaError(path='', code='type', value={})], list(schema.get_schema_errors({})))
        self.assertEqual([SchemaError(path='', code='type', value=True)], list(schema.get_schema_errors(True)))

    def test_dump_and_load(self):
        schema = AnyOfSchema(schemas=(BooleanSchema(), StringSchema()))
        dumped = dump(schema)
        expected_dump = dict(anyOf=[dict(type='boolean'), dict(type='string')])
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_tuple(self):
        schema = schema_for_type(Union[bool, str]).json_schema
        dumped = dump(schema)
        expected_dump = {'anyOf': [
            {'items': False, 'prefixItems': [{'const': 'bool'}, {'type': 'boolean'}], 'type': 'array'},
            {'items': False, 'prefixItems': [{'const': 'str'}, {'type': 'string'}], 'type': 'array'}
        ]}
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_name(self):
        schema = AnyOfSchema(schemas=(BooleanSchema(), StringSchema()), name='A Bool or String')
        dumped = dump(schema)
        expected_dump = dict(
            anyOf=[dict(type='boolean'), dict(type='string')],
            name='A Bool or String'
        )
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_post_init_simplify(self):
        schema = AnyOfSchema(schemas=(BooleanSchema(), AnyOfSchema(schemas=(StringSchema(), IntegerSchema()))))
        dumped = dump(schema)
        expected_dump = dict(
            anyOf=[dict(type='boolean'), dict(type='string'), dict(type='integer')],
        )
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)
