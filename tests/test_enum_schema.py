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
            {"name": "MyEnum", "enum": ["FOO", "BAR", "ZAP", "BANG"]}, MyEnum
        )
        self.assertEqual(expected, schema)

    def test_load_and_dump(self):
        schema = schema_from_type(MyEnum)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(
            loaded.schema, {"name": "MyEnum", "enum": ["FOO", "BAR", "ZAP", "BANG"]}
        )
        self.assertEqual("MyEnum", loaded.python_type.__name__)
        self.assertTrue(Enum in loaded.python_type.__mro__)
        # noinspection PyTypeChecker
        self.assertEqual(
            [e.name for e in MyEnum], [e.value for e in loaded.python_type]
        )
        # noinspection PyTypeChecker
        self.assertEqual(
            [e.name for e in MyEnum], [e.name for e in loaded.python_type]
        )

    def test_validate(self):
        schema = schema_from_type(MyEnum)
        schema.validate("ZAP")
        with self.assertRaises(ValidationError):
            schema.validate("PING")
