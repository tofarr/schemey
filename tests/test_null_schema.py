from unittest import TestCase

from schemey.null_schema import NullSchema
from schemey.schema_error import SchemaError


class TestObjectSchema(TestCase):

    def test_null_schema(self):
        schema = NullSchema()
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('True', ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 'True')]
        assert list(schema.get_schema_errors(None)) == []

    def test_to_json_schema(self):
        assert NullSchema().to_json_schema() == dict(type='null')

    def test_class(self):
        assert NullSchema() is NullSchema()  # Make sure it is a singleton
        assert str(NullSchema()) == "NullSchema()"
        assert NullSchema().default_value is None

    def test_item_type(self):
        none_type = type(None)
        assert NullSchema().item_type == none_type
