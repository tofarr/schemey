from typing import Optional, Type, Dict

from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext

SCHEMA_FACTORY = "__schema_factory__"


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(context, path, ref_schemas)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        """No implementation"""
