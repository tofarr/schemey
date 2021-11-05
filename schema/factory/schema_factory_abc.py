from abc import abstractmethod, ABC
from functools import total_ordering
from typing import TypeVar, Type, Optional

from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_context import SchemaContext

T = TypeVar('T')


@total_ordering
class SchemaFactoryABC(ABC):
    priority: int = 100

    @abstractmethod
    def create(self, type_: Type[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        """
        Create a schema for the type given, or return None if that was not possible
        """

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)