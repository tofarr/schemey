from typing import Optional, List
from unittest import TestCase

from schemey import optional_schema
from schemey import ArraySchema
from schemey import DeferredSchema
from schemey import ObjectSchema
from schemey import PropertySchema
from schemey import schema_for_type, get_default_schema_context
from schemey import SchemaError
from schemey import StringSchema
from old.tests.fixtures import Node


class TestSelfRefSchema(TestCase):

    def test_self_ref_schema(self):
        schema_context = get_default_schema_context()
        schema = schema_for_type(Node, schema_context)
        expected = ObjectSchema(Node, (
            PropertySchema(name='id', schema=StringSchema(), required=True),
            PropertySchema(name='parent', schema=optional_schema(DeferredSchema(schema_context, Node))),
            PropertySchema(name='children', schema=ArraySchema(item_schema=DeferredSchema(schema_context, Node),
                                                               item_type_=List[Node]))
        ))
        assert expected == schema

    def test_self_ref_schema_validate(self):
        schema = schema_for_type(Node)
        schema.validate(Node('root', None, [Node('child-a'), Node('child-b')]))

    def test_self_ref_schema_validate_invalid(self):
        schema = schema_for_type(Node)
        with self.assertRaises(SchemaError):
            schema.validate(Node('root', [Node('child-a'), Node('child-b')]))

    def test_item_type(self):
        schema = schema_for_type(Node)
        property_schema = next(s for s in schema.property_schemas if s.name == 'parent')
        assert property_schema.item_type == Optional[Node]
        assert property_schema.default_value is None

    def test_default_value(self):
        schema = DeferredSchema(get_default_schema_context(), Node)
        assert schema.default_value is None