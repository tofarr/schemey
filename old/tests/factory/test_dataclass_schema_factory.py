from unittest import TestCase

from schemey import DataclassSchemaFactory
from schemey import get_default_schema_context


class TestDataclassSchemaFactory(TestCase):

    def test_non_dataclass(self):
        factory = DataclassSchemaFactory()
        assert factory.create(str, get_default_schema_context(), None) is None
