from typing import Tuple
from unittest import TestCase

from marshy import dump, load

from schemey import schema_from_type, Schema


class TestTupleSchema(TestCase):
    def test_create_tuple_schema(self):
        my_tuple = Tuple[int, str, bool]
        schema = schema_from_type(my_tuple)
        dumped = dump(schema)
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
        my_tuple = Tuple[int, str, bool]
        schema = schema_from_type(my_tuple)
        dumped = dump(schema)
        loaded = load(Schema, dumped)
        self.assertEqual(schema, loaded)
