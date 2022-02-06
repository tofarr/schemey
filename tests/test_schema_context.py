from unittest import TestCase

import tests
from schemey import __version__
from schemey.boolean_schema import BooleanSchema
from schemey.factory.impl_schema_factory import ImplSchemaFactory
from schemey.loader.boolean_schema_loader import BooleanSchemaLoader
from schemey.schema_error import SchemaError
from schemey.schema_context import schema_for_type


class TestSchemaContext(TestCase):

    def test_version(self):
        assert tests
        assert __version__

    def test_uncreatable_schema(self):
        with self.assertRaises(ValueError):
            schema_for_type(ValueError)

    def test_schema_compare(self):
        assert not BooleanSchema().__ne__(BooleanSchema())

    def test_schema_loader_compare(self):
        assert not BooleanSchemaLoader().__ne__(BooleanSchemaLoader())

    def test_schema_factory_compare(self):
        assert not ImplSchemaFactory().__ne__(ImplSchemaFactory())

    def test_validate(self):
        schema_for_type(int).validate(10)
        with self.assertRaises(SchemaError):
            schema_for_type(int).validate(10.5)
