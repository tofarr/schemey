from unittest import TestCase

from schemey.boolean_schema import BooleanSchema
from schemey.schema_context import schema_for_type
from schemey.schema_error import SchemaError


class TestObjectSchema(TestCase):

    def test_boolean_schema(self):
        schema = BooleanSchema()
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('True')) == [SchemaError('', 'type', 'True')]
        assert list(schema.get_schema_errors(True)) == []

    def test_to_json_schema(self):
        assert dict(type='boolean') == BooleanSchema().to_json_schema()
        assert dict(type='boolean') == BooleanSchema(False).to_json_schema()
        assert dict(type='boolean', default=True) == BooleanSchema(True).to_json_schema()

    def test_class(self):
        assert BooleanSchema(False) is BooleanSchema()  # Make sure it is a singleton
        assert str(BooleanSchema()) == "BooleanSchema()"
        assert BooleanSchema(True) is BooleanSchema(True)
        assert BooleanSchema(True).default_value is True
        assert BooleanSchema(False).default_value is False

    def test_item_type(self):
        schema = schema_for_type(bool)
        assert schema.item_type == bool

