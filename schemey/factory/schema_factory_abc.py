from abc import abstractmethod, ABC
from functools import total_ordering
from typing import Type, Optional, Dict

from marshy.types import ExternalItemType

from schemey.schema import Schema
from schemey.schema_context import SchemaContext


@total_ordering
class SchemaFactoryABC(ABC):
    @property
    def priority(self):
        return 100

    @abstractmethod
    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        """
        Create a schema for the type given, or return None if that was not possible
        """

    @abstractmethod
    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        """
        Create a schema for the type given, or return None if that was not possible
        """

    def __lt__(self, other):
        return self.priority < getattr(other, "priority", None)
