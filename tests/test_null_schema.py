from unittest import TestCase

from marshy import dump, load

from schemey.schema_abc import SchemaABC
from schemey.null_schema import NullSchema
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context


class TestBooleanSchema(TestCase):

    def test_factory(self):
        context = get_default_schema_context()
        schema = context.get_schema(type(None))
        expected = NullSchema()
        self.assertEqual(expected, schema)

    def test_null_schema(self):
        schema = NullSchema()
        errors = list(schema.get_schema_errors('True', ['foo', 'bar']))
        # noinspection PyTypeChecker
        self.assertEqual(errors, [SchemaError('foo/bar', 'type', 'True')])
        self.assertEqual(list(schema.get_schema_errors(None)), [])

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.get_schema(type(None))
        schema.validate(None)

    def test_validate_fail(self):
        context = get_default_schema_context()
        schema = context.get_schema(type(None))
        with self.assertRaises(SchemaError):
            schema.validate('Not None!')

    def test_dump_and_load(self):
        schema = NullSchema()
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)
