from unittest import TestCase

from persisty.schema.factory.dataclass_schema_factory import DataclassSchemaFactory
from persisty.schema.schema_context import get_default_schema_context


class TestDataclassSchemaFactory(TestCase):

    def test_non_dataclass(self):
        factory = DataclassSchemaFactory()
        assert factory.create(str, get_default_schema_context()) is None
