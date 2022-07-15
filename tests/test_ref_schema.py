from unittest import TestCase

from marshy import load

from schemey.schema_abc import SchemaABC


class TestSchemaContext(TestCase):
    def test_bad_ref(self):
        to_load = {"$ref": "#foo/bar"}
        with self.assertRaises(ValueError):
            load(SchemaABC, to_load)
