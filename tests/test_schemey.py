from copy import deepcopy
from unittest import TestCase

from schemey import schema_from_json, schema_from_type
from schemey.schema import update_refs


class TestSchemey(TestCase):
    def test_schema_from_json(self):
        self.assertEqual(int, schema_from_json({"type": "integer"}).python_type)

    def test_schema_from_type_impossible(self):
        class Foo:
            pass

        with self.assertRaises(ValueError):
            schema_from_type(Foo)

    def test_schema_from_json_impossible(self):
        with self.assertRaises(ValueError):
            schema_from_json({"type": "foobar"})

    def test_update_refs(self):
        un_updated = {
            "a": {"$ref": "ref_a"},
            "b": [{"$ref": "ref_b"}, {"$ref": "ref_a"}],
            "c": 10,
        }
        expected = {
            "a": {"$ref": "ref_c"},
            "b": [{"$ref": "ref_b"}, {"$ref": "ref_c"}],
            "c": 10,
        }
        schema = deepcopy(un_updated)
        updated = update_refs(schema, "ref_a", "ref_c")
        self.assertEqual(expected, updated)
        self.assertEqual(schema, un_updated)
