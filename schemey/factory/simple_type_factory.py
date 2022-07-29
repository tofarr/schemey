from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Type, Dict

from marshy.types import ExternalItemType

from schemey.schema import Schema
from schemey.schema_context import SchemaContext
from schemey.factory.schema_factory_abc import SchemaFactoryABC


@dataclass
class SimpleTypeFactory(SchemaFactoryABC):
    python_type: Type
    json_type: str
    priority: int = 200

    def from_type(
        self, type_: Type, context: SchemaContext, path: str
    ) -> Optional[Schema]:
        if type_ == self.python_type:
            return Schema({"type": self.json_type}, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        type_ = item.get("type")
        if type_ == self.json_type:
            return Schema(item, self.python_type)
