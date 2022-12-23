from typing import Dict, Optional, Type

from marshy.types import ExternalItemType

from schemey import SchemaContext, Schema
from schemey.factory.schema_factory_abc import SchemaFactoryABC


class RefSchemaFactory(SchemaFactoryABC):
    """Schema factory for resolving json refs."""

    priority: int = 220

    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        pass

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        ref = item.get("$ref")
        if ref:
            return ref_schemas.get(ref)
