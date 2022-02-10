from dataclasses import dataclass
from unittest import TestCase

from schemey.const_schema import ConstSchema
from schemey.schema_error import SchemaError


class TestBooleanSchema(TestCase):

    def test_get_schema_errors(self):
        schema = ConstSchema('foobar')
        self.assertEqual([], list(schema.get_schema_errors('foobar')))
        self.assertEqual([SchemaError('', 'invalid_value', 10)], list(schema.get_schema_errors(10)))
        self.assertEqual([SchemaError('a/b', 'invalid_value', 'nope')],
                         list(schema.get_schema_errors('nope', ['a', 'b'])))

    def test_get_normalized_type(self):
        standard_type = ConstSchema('boom').get_normalized_type({}, dataclass)
        self.assertEqual(str, standard_type)
