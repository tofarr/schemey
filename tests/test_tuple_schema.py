from dataclasses import dataclass, is_dataclass, fields, MISSING
from typing import Tuple, Union
from unittest import TestCase

from marshy import dump

from schemey.boolean_schema import BooleanSchema
from schemey.factory.tuple_schema_factory import TupleSchemaFactory
from schemey.integer_schema import IntegerSchema
from schemey.json_schema_context import JsonSchemaContext
from schemey.param_schema import ParamSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import schema_for_type
from schemey.schema_error import SchemaError
from schemey.string_schema import StringSchema
from schemey.tuple_schema import TupleSchema


class TestTupleSchema(TestCase):
    def test_create_tuple_schema(self):
        my_tuple = Tuple[int, str, bool]
        schema = schema_for_type(my_tuple).json_schema
        dumped = dump(schema, SchemaABC)
        expected = {
            "items": False,
            "prefixItems": [
                {"type": "integer"},
                {"type": "string"},
                {"type": "boolean"},
            ],
            "type": "array",
        }
        self.assertEqual(expected, dumped)

    def test_load_dump_schema(self):
        schema = TupleSchema(
            schemas=(StringSchema(), BooleanSchema()), description="A str or bool"
        )
        dumped = dump(schema, SchemaABC)
        expected = {
            "items": False,
            "prefixItems": [{"type": "string"}, {"type": "boolean"}],
            "type": "array",
            "description": "A str or bool",
        }
        self.assertEqual(expected, dumped)

    def test_factory_ellipsis(self):
        type_ = Tuple[int, ...]
        json_schema_context = JsonSchemaContext()
        self.assertIsNone(TupleSchemaFactory().create(type_, json_schema_context))

    def test_get_normalized_type(self):
        types = (int, str, bool)
        type_ = Tuple[int, str, bool]
        schema = schema_for_type(type_)
        normalized_type = schema.json_schema.get_normalized_type({}, dataclass)
        assert is_dataclass(normalized_type)
        # noinspection PyDataclass
        for f in fields(normalized_type):
            self.assertIs(MISSING, f.default)
            self.assertIs(MISSING, f.default_factory)
            assert f.name.startswith("t")
            index = int(f.name[1:])
            self.assertEqual(types[index], f.type)

    def test_get_param_schemas(self):
        type_ = Tuple[int, str, bool]
        schema = schema_for_type(type_)
        param_schemas = schema.get_param_schemas("foo")
        expected_param_schemas = [
            ParamSchema("foo.0", IntegerSchema()),
            ParamSchema("foo.1", StringSchema()),
            ParamSchema("foo.2", BooleanSchema()),
        ]
        self.assertEqual(expected_param_schemas, param_schemas)

    def test_get_param_schemas_invalid(self):
        type_ = Tuple[int, Union[str, int]]
        schema = schema_for_type(type_)
        param_schemas = schema.get_param_schemas("foo")
        self.assertIsNone(param_schemas)

    def test_url_param_schemas(self):
        type_ = Tuple[int, str, bool]
        schema = schema_for_type(type_)
        url_params = {"0": ["5"], "1": ["foo"], "2": ["1"]}
        loaded = schema.from_url_params(url_params)
        self.assertEqual((5, "foo", True), loaded)
        dumped = list(schema.to_url_params(loaded))
        self.assertEqual([("0", "5"), ("1", "foo"), ("2", "1")], dumped)

    def test_url_param_schemas_invalid(self):
        schema = TupleSchema((StringSchema(), IntegerSchema()))
        with self.assertRaises(SchemaError):
            schema.from_url_params("", {"1": ["2"]})
