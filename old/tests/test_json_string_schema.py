from typing import Dict
from unittest import TestCase
from uuid import uuid4

from marshy.types import ExternalItemType, ExternalType
from marshy.utils import resolve_forward_refs

from schemey import JsonStringSchemaFactory
from schemey import GraphqlAttr
from schemey import schema_for_type, new_default_schema_context
from schemey import SchemaError


class TestObjectSchema(TestCase):

    def test_validate(self):
        schema = schema_for_type(ExternalItemType)
        assert schema.item_type == resolve_forward_refs(ExternalItemType)
        schema.validate('{"a":"b"}')

    def test_validate_array(self):
        schema = schema_for_type(ExternalType)
        assert schema.item_type == resolve_forward_refs(ExternalType)
        schema.validate('[1,2,3]')

    def test_validate_invalid_json(self):
        schema = schema_for_type(ExternalItemType)
        errors = list(schema.get_schema_errors('{"a":', ['foo', 'bar']))
        expected = [SchemaError('foo/bar', 'format:json', '{"a":')]
        assert errors == expected

    def test_validate_wrong_type(self):
        schema = schema_for_type(ExternalItemType)
        uuid = uuid4()
        errors = list(schema.get_schema_errors(uuid))
        expected = [SchemaError('', 'type', uuid)]
        assert errors == expected

    def test_validate_wrong_json_type(self):
        schema = schema_for_type(ExternalItemType)
        errors = list(schema.get_schema_errors('[1,2,3]'))
        expected = [SchemaError('', 'not_an_object', [1, 2, 3])]
        assert errors == expected

    def test_default_value(self):
        assert schema_for_type(ExternalItemType).default_value is None
        default_value = schema_for_type(ExternalItemType, default_value=dict(foo='bar')).default_value
        assert default_value == dict(foo='bar')

    def test_to_json_schema(self):
        schema = schema_for_type(ExternalItemType).dump_json_schema()
        assert schema == dict(type='string', format='json_object')
        schema = schema_for_type(ExternalType).dump_json_schema()
        assert schema == dict(type='string', format='json')

    def test_to_graphql_attr(self):
        assert schema_for_type(ExternalItemType).to_graphql_attr() == GraphqlAttr('String')

    def test_match(self):
        assert JsonStringSchemaFactory().create(Dict[int, int], new_default_schema_context(), {}) is None
