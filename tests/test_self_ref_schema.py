from unittest import TestCase

from schema.any_of_schema import optional_schema
from schema.array_schema import ArraySchema
from schema.object_schema import ObjectSchema
from schema.property_schema import PropertySchema
from schema.ref_schema import RefSchema
from schema.schema_context import schema_for_type
from schema.string_schema import StringSchema
from schema.with_defs_schema import WithDefsSchema
from tests.fixtures import Node


class TestSelfRefSchema(TestCase):

    def test_self_ref_schema(self):
        schema = schema_for_type(Node)
        expected = WithDefsSchema(
            defs={'Node': ObjectSchema(property_schemas=(
                PropertySchema(name='id', schema=StringSchema()),
                PropertySchema(name='parent', schema=optional_schema(RefSchema(ref='Node'))),
                PropertySchema(name='children', schema=ArraySchema(item_schema=RefSchema(ref='Node'))))
            )},
            schema=RefSchema(ref='Node')
        )
        assert expected == schema
