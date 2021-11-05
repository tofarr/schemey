from unittest import TestCase

from marshy.default_context import new_default_context

from persisty.schema.boolean_schema import BooleanSchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError


class TestObjectSchema(TestCase):

    def test_boolean_schema(self):
        schema = BooleanSchema()
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('True')) == [SchemaError('', 'type', 'True')]
        assert list(schema.get_schema_errors(True)) == []

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(BooleanSchema, dict(type='boolean')) == BooleanSchema()
        assert context.load(SchemaABC, dict(type='boolean')) == BooleanSchema()
        assert context.dump(BooleanSchema()) == dict(type='boolean')

    def test_class(self):
        assert BooleanSchema() is BooleanSchema()  # Make sure it is a singleton
        assert str(BooleanSchema()) == "BooleanSchema()"
