from dataclasses import dataclass
from typing import Type, Optional
from unittest import TestCase

from schemey import SchemaFactoryABC
from schemey import SchemaABC, T
from schemey import SchemaContext


@dataclass
class MySchemaFactory(SchemaFactoryABC):
    priority: int = 100

    def create(self, type_: Type[T], default_value, context: SchemaContext) -> Optional[SchemaABC[T]]:
        """ Not Used """


class TestSchemaFactoryABC(TestCase):

    def test_ordering(self):
        length = 10
        factories = [MySchemaFactory(length-1-i) for i in range(length)]
        factories.sort()
        for index, factory in enumerate(factories):
            assert index == factory.priority

    def test_ne(self):
        assert MySchemaFactory(10) != MySchemaFactory(11)
        assert MySchemaFactory(10) == MySchemaFactory(10)
