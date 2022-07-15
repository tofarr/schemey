from dataclasses import dataclass
from typing import Union
from unittest import TestCase

from marshy import load, dump

from schemey.any_of_schema import AnyOfSchema
from schemey.boolean_schema import BooleanSchema
from schemey.const_schema import ConstSchema
from schemey.integer_schema import IntegerSchema
from schemey.schema_abc import SchemaABC, NoDefault
from schemey.schema_error import SchemaError
from schemey.schema_context import get_default_schema_context, schema_for_type
from schemey.string_schema import StringSchema
from schemey.tuple_schema import TupleSchema


class TestAnyOfSchema(TestCase):
    def test_factory(self):
        context = get_default_schema_context()
        schema = context.get_schema(Union[bool, str])
        expected = AnyOfSchema(
            schemas=(
                TupleSchema((ConstSchema("bool"), BooleanSchema())),
                TupleSchema((ConstSchema("str"), StringSchema())),
            )
        )
        self.assertEqual(expected, schema)

    def test_get_schema_errors(self):
        context = get_default_schema_context()
        schema = context.get_schema(Union[bool, str])
        self.assertEqual([], list(schema.get_schema_errors(["bool", True])))
        self.assertEqual([], list(schema.get_schema_errors(["bool", False])))
        self.assertEqual([], list(schema.get_schema_errors(["str", "True"])))
        self.assertEqual([], list(schema.get_schema_errors(["str", "Yo"])))
        self.assertEqual(
            [SchemaError(path="", code="type", value={})],
            list(schema.get_schema_errors({})),
        )
        self.assertEqual(
            [SchemaError(path="", code="type", value=True)],
            list(schema.get_schema_errors(True)),
        )

    def test_dump_and_load(self):
        schema = AnyOfSchema(schemas=(BooleanSchema(), StringSchema()))
        dumped = dump(schema)
        expected_dump = dict(anyOf=[dict(type="boolean"), dict(type="string")])
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_tuple(self):
        schema = schema_for_type(Union[bool, str]).json_schema
        dumped = dump(schema)
        expected_dump = {
            "anyOf": [
                {
                    "items": False,
                    "prefixItems": [{"const": "bool"}, {"type": "boolean"}],
                    "type": "array",
                },
                {
                    "items": False,
                    "prefixItems": [{"const": "str"}, {"type": "string"}],
                    "type": "array",
                },
            ]
        }
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_dump_and_load_with_name(self):
        schema = AnyOfSchema(
            schemas=(BooleanSchema(), StringSchema()),
            name="A Bool or String",
            description="A description",
        )
        dumped = dump(schema)
        expected_dump = dict(
            anyOf=[dict(type="boolean"), dict(type="string")],
            name="A Bool or String",
            description="A description",
        )
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_post_init_simplify(self):
        schema = AnyOfSchema(
            schemas=(
                BooleanSchema(),
                AnyOfSchema(schemas=(StringSchema(), IntegerSchema())),
            )
        )
        dumped = dump(schema)
        expected_dump = dict(
            anyOf=[dict(type="boolean"), dict(type="string"), dict(type="integer")],
        )
        self.assertEqual(expected_dump, dumped)
        loaded = load(SchemaABC, dumped)
        self.assertEqual(schema, loaded)

    def test_get_normalized_type(self):
        schema = AnyOfSchema([IntegerSchema(), StringSchema()])
        standard_type = schema.get_normalized_type({}, dataclass)
        expected = Union[int, str]
        self.assertEqual(expected, standard_type)

    def test_get_normalized_type_named(self):
        schema = AnyOfSchema(schemas=[IntegerSchema(), StringSchema()], name="Foo")
        expected = Union[int, str]
        standard_type = schema.get_normalized_type(dict(Foo=expected), dataclass)
        self.assertEqual(expected, standard_type)

    def test_url_params(self):
        schema = AnyOfSchema([IntegerSchema(), StringSchema()])
        self.assertEqual(NoDefault, schema.from_url_params("", {}))
        with self.assertRaises(NotImplementedError):
            schema.to_url_params("", {})
