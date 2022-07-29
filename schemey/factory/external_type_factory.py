from dataclasses import dataclass
from typing import Dict, Optional, Type

from marshy.types import ExternalItemType, ExternalType

from schemey import SchemaContext, Schema
from schemey.factory.schema_factory_abc import SchemaFactoryABC


@dataclass
class ExternalTypeFactory(SchemaFactoryABC):
    priority: int = 120

    def from_type(
        self, type_: Type, context: SchemaContext, path: str
    ) -> Optional[Schema]:
        if type_ == ExternalItemType:
            return Schema({"type": "object", "additionalProperties": True}, type_)
        elif type_ == ExternalType:
            return Schema({}, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        if item == {}:
            return Schema(item, ExternalType)
        type_ = item.get("type")
        properties = item.get("properties")
        additional_properties = item.get("additionalProperties")
        if type_ == "object" and not properties and additional_properties is True:
            return Schema(item, ExternalItemType)
