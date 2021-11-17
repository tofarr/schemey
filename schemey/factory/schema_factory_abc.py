from abc import abstractmethod, ABC
from functools import total_ordering
from typing import TypeVar, Type, Optional

from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext

T = TypeVar('T')
NONE_TYPE = type(None)


@total_ordering
class SchemaFactoryABC(ABC):
    priority: int = 100

    @abstractmethod
    def create(self, type_: Type[T], default_value: Optional[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        """
        Create a schemey for the type given, or return None if that was not possible
        """

    def __ne__(self, other):
        return self.priority != getattr(other, 'priority', None)

    def __lt__(self, other):
        return self.priority < getattr(other, 'priority', None)
