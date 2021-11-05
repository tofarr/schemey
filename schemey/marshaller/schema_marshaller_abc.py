from abc import ABC, abstractmethod
from typing import TypeVar

from marshy.marshaller.marshaller_abc import MarshallerABC
from marshy.types import ExternalItemType

from schemey.schema_abc import SchemaABC

T = TypeVar('T', bound=SchemaABC)

TYPE = 'type'


class SchemaMarshallerABC(MarshallerABC[T], ABC):
    """
    Since not all types from json have a simple "type" attribute we can check of, we need custom polymorphism
    when unmarshalling.
    """
    priority: int = 100

    @abstractmethod
    def can_load(self, item: ExternalItemType) -> bool:
        """ Determine if this marshaller can load the item given """

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)
