from dataclasses import dataclass
from enum import Enum
from unittest import TestCase

from jsonschema import ValidationError
from marshy import load, dump

from schemey import schema_from_type, Schema


class MyEnum(Enum):
    FOO = "foo"
    BAR = "bar"
    ZAP = "zap"
    BANG = "bang"


class TestEnumSchema(TestCase):
    def test_factory(self):
        schema = schema_from_type(MyEnum)
        expected = Schema(
            {"name": "MyEnum", "enum": ["foo", "bar", "zap", "bang"]}, MyEnum
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump(self):
        schema = schema_from_type(MyEnum)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(
            loaded.schema, {"name": "MyEnum", "enum": ["foo", "bar", "zap", "bang"]}
        )
        self.assertEqual("MyEnum", loaded.python_type.__name__)
        self.assertTrue(Enum in loaded.python_type.__mro__)
        # noinspection PyTypeChecker
        self.assertEqual(
            [e.value for e in MyEnum], [e.value for e in loaded.python_type]
        )
        # noinspection PyTypeChecker
        self.assertEqual(
            [e.value for e in MyEnum], [e.name for e in loaded.python_type]
        )

    def test_validate(self):
        schema = schema_from_type(MyEnum)
        schema.validate("zap")
        with self.assertRaises(ValidationError):
            schema.validate("ping")
