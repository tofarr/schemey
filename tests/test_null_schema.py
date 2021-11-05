from unittest import TestCase

from marshy.default_context import new_default_context

from schemey.null_schema import NullSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_error import SchemaError


class TestObjectSchema(TestCase):

    def test_null_schema(self):
        schema = NullSchema()
        # noinspection PyTypeChecker
        assert list(schema.get_schema_errors('True', {}, ['foo', 'bar'])) == [SchemaError('foo/bar', 'type', 'True')]
        assert list(schema.get_schema_errors(None, {})) == []

    def test_marshalling(self):
        context = new_default_context()
        assert context.load(NullSchema, dict(type='null')) == NullSchema()
        assert context.load(SchemaABC, dict(type='null')) == NullSchema()
        assert context.dump(NullSchema()) == dict(type='null')

    def test_class(self):
        assert NullSchema() is NullSchema()  # Make sure it is a singleton
        assert str(NullSchema()) == "NullSchema()"
