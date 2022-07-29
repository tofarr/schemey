from unittest import TestCase

from schemey import schema_from_json, schema_from_type
from schemey.version import __version__


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

    def test_version(self):
        self.assertTrue(isinstance(__version__, str))
