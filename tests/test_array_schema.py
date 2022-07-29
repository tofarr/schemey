from typing import List, Set, Union, Tuple
from unittest import TestCase

from jsonschema import ValidationError
from marshy import dump, load

# noinspection PyTypeChecker
from schemey import schema_from_type, Schema


class TestArraySchema(TestCase):
    def test_factory(self):
        schema = schema_from_type(List[bool])
        expected = Schema(
            schema={"type": "array", "items": {"type": "boolean"}},
            python_type=List[bool],
        )
        self.assertEqual(expected, schema)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(expected, loaded)
        schema.validate([True, False])
        with self.assertRaises(ValidationError):
            schema.validate("string")
        with self.assertRaises(ValidationError):
            schema.validate([True, "string"])

    def test_no_type(self):
        schema = schema_from_type(List)
        expected = Schema(
            schema={"type": "array"},
            python_type=List,
        )
        self.assertEqual(expected, schema)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(expected, loaded)
        schema.validate([True, "foobar"])
        with self.assertRaises(ValidationError):
            schema.validate("string")

    def test_set(self):
        schema = schema_from_type(Set[Union[type(None), bool, str]])
        expected = Schema(
            schema={
                "type": "array",
                "items": {
                    "anyOf": [{"type": "null"}, {"type": "boolean"}, {"type": "string"}]
                },
                "uniqueItems": True,
            },
            python_type=Set[Union[type(None), bool, str]],
        )
        self.assertEqual(expected, schema)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(expected, loaded)
        schema.validate([True, "foobar", None])
        with self.assertRaises(ValidationError):
            schema.validate([True, "string", 10])

    def test_tuple(self):
        schema = schema_from_type(Tuple[int, ...])
        expected = Schema(
            schema={"type": "array", "items": {"type": "integer"}, "tuple": True},
            python_type=Tuple[int, ...],
        )
        self.assertEqual(expected, schema)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(expected, loaded)
        schema.validate([1, 2])
        schema.validate([1.0, 2])
        with self.assertRaises(ValidationError):
            schema.validate([1.5, 2])

    def test_max_items(self):
        schema = Schema(
            schema={"type": "array", "items": {"type": "boolean"}, "maxItems": 2},
            python_type=List[bool],
        )
        schema.validate([True, False])
        with self.assertRaises(ValidationError):
            schema.validate([True, False, False])

    def test_unique(self):
        schema = Schema(
            schema={"type": "array", "items": {"type": "boolean"}, "uniqueItems": True},
            python_type=List[bool],
        )
        schema.validate([True, False])
        with self.assertRaises(ValidationError):
            schema.validate([True, False, False])
