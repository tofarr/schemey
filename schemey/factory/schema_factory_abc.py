from abc import abstractmethod, ABC
from typing import Type, Optional, Dict

from marshy.types import ExternalItemType

from schemey.schema import Schema

_SchemaContext = "schemey.schema_context.SchemaContext"


class SchemaFactoryABC(ABC):
    priority: int = 100

    @abstractmethod
    def from_type(
        self,
        type_: Type,
        context: _SchemaContext,
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
        context: _SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        """
        Create a schema for the type given, or return None if that was not possible
        """
