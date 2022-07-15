from typing import Optional, Type

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schema_abc import SchemaABC

SCHEMA_FACTORY = "__schema_factory__"


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(json_context)
