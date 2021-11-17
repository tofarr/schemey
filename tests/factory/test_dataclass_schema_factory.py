from unittest import TestCase

from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.schema_context import get_default_schema_context


class TestDataclassSchemaFactory(TestCase):

    def test_non_dataclass(self):
        factory = DataclassSchemaFactory()
        assert factory.create(str, None, get_default_schema_context()) is None
