from typing import Optional, Dict

from schema.factory.schema_factory_abc import SchemaFactoryABC
from schema.schema_abc import SchemaABC
from schema.schema_context import SchemaContext

SCHEMA_FACTORY = '__schema_factory__'


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def create(self, type_, context: SchemaContext, defs: Dict[str, SchemaABC]) -> Optional[SchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(context, defs)
