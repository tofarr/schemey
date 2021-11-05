from unittest import TestCase

from marshy.default_context import new_default_context

from persisty.schema.null_schema import NullSchema
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_error import SchemaError


class TestObjectSchema(TestCase):

    def test_null_schema(self):
        schema = NullSchema()
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('True', ['foo','bar'])) == [SchemaError('foo/bar', 'type', 'True')]
        assert list(schema.get_schema_errors(None)) == []

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(NullSchema, dict(type=None)) == NullSchema()
        assert context.load(SchemaABC, dict(type=None)) == NullSchema()
        assert context.dump(NullSchema()) == dict(type=None)

    def test_class(self):
        assert NullSchema() is NullSchema()  # Make sure it is a singleton
        assert str(NullSchema()) == "NullSchema()"
