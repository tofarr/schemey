from unittest import TestCase

from schemey.integer_schema import IntegerSchema
from schemey.json_schema_context import JsonSchemaContext
from schemey.param_schema import ParamSchema


class TestParamSchema(TestCase):

    def test_dump_json(self):
        schema = ParamSchema('foo', IntegerSchema(), False, 'path')
        dumped = schema.dump_json(JsonSchemaContext())
        expected = {'in': 'path', 'name': 'foo', 'required': False, 'schema': {'type': 'integer'}}
        self.assertEqual(expected, dumped)
