from typing import Type, Optional

from persisty.schema.factory.schema_factory_abc import SchemaFactoryABC
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_context import SchemaContext

SCHEMA_FACTORY = '__schema_factory__'


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def create(self, type_: Type, context: SchemaContext) -> Optional[SchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(context)
