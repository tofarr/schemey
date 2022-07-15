from dataclasses import dataclass
from unittest import TestCase

from marshy import load, dump

from schemey.boolean_schema import BooleanSchema
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC, NoDefault
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context


class TestBooleanSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.get_schema(bool)
        expected = BooleanSchema()
        self.assertEqual(expected, schema)

    def test_get_schema_errors(self):
        context = get_default_schema_context()
        schema = context.get_schema(bool)
        # Boolean schema actually accepts anything and converts it to truthy / falsy
        self.assertEqual([], list(schema.get_schema_errors(True)))
        self.assertEqual([], list(schema.get_schema_errors(False)))
        self.assertEqual(
            [SchemaError("", "type", "True")], list(schema.get_schema_errors("True"))
        )
        self.assertEqual(
            [SchemaError("a/b", "type", "True")],
            list(schema.get_schema_errors("True", ["a", "b"])),
        )

    def test_validate(self):
        context = get_default_schema_context()
        schema = context.get_schema(bool)
        with self.assertRaises(SchemaError):
            # noinspection PyTypeChecker
            schema.validate(10)

    def test_dump_and_load(self):
        schema = BooleanSchema()
        dumped = dump(schema)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_description(self):
        schema = BooleanSchema(description="A flag")
        dumped = dump(schema)
        expected = dict(type="boolean", description="A flag")
        self.assertEqual(expected, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_get_param_schemas(self):
        schema = BooleanSchema()
        param_schemas = schema.get_param_schemas("foo")
        expected = [ParamSchema("foo", schema)]
        self.assertEqual(expected, param_schemas)

    def test_from_url_params(self):
        schema = BooleanSchema()
        self.assertTrue(schema.from_url_params("foo", dict(foo=["1"])))
        self.assertFalse(schema.from_url_params("foo", dict(foo=["0"])))
        self.assertTrue(schema.from_url_params("bar", dict(bar=["tRuE"])))
        self.assertFalse(schema.from_url_params("bar", dict(bar=["fAlSe"])))
        self.assertEqual(NoDefault, schema.from_url_params("bar", dict()))

    def test_to_url_params(self):
        schema = BooleanSchema()
        self.assertEqual([("foo", "1")], list(schema.to_url_params("foo", True)))
        self.assertEqual([("bar", "0")], list(schema.to_url_params("bar", False)))

    def test_get_normalized_type(self):
        schema = BooleanSchema()
        self.assertEqual(bool, schema.get_normalized_type({}, dataclass))
