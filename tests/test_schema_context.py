from unittest import TestCase

from schemey import __version__
from schemey.schemey_context import schema_for_type


class TestSchemaContext(TestCase):

    def test_version(self):
        assert __version__

    def test_uncreatable_schema(self):
        with self.assertRaises(ValueError):
            schema_for_type(ValueError)
