from typing import Optional

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext

SCHEMA_FACTORY = '__schema_factory__'


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def create(self, type_, default_value, context: SchemaContext) -> Optional[SchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(default_value, context)
