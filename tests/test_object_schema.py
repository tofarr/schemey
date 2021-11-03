from unittest import TestCase

from marshy.default_context import new_default_context

from persisty.schema.any_of_schema import optional_schema
from persisty.schema.boolean_schema import BooleanSchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.number_schema import NumberSchema
from persisty.schema.object_schema import ObjectSchema
from persisty.schema.property_schema import PropertySchema
from persisty.schema.schema_error import SchemaError
from persisty.schema.string_schema import StringSchema
from tests.fixtures.items import Band


class TestObjectSchema(TestCase):

    def test_object_schema(self):
        schema = ObjectSchema([
            PropertySchema('id', StringSchema(min_length=1)),
            PropertySchema('year_formed', optional_schema(NumberSchema(int, minimum=1900))),
        ])
        assert list(schema.get_schema_errors(Band())) == [SchemaError('id', 'type')]
        assert list(schema.get_schema_errors(Band(''))) == [SchemaError('id', 'min_length', '')]
        assert list(schema.get_schema_errors(Band('mozart', 'Mozart', 1756))) == \
               [SchemaError('year_formed', 'minimum', 1756)]

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(ObjectSchema, dict(type='object')) == ObjectSchema()

        json_schema = {
            "type": "object",
            "properties": {
                "some_str": {"type": "string"},
                "some_bool": {"type": "boolean"}
            }
        }
        schema = ObjectSchema(tuple((
            PropertySchema('some_str', StringSchema()),
            PropertySchema('some_bool', BooleanSchema())
        )))
        assert context.load(SchemaABC, json_schema) == schema
        assert context.dump(schema) == json_schema
