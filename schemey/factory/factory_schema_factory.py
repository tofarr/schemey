from typing import Optional, Type, Union

from marshy import ExternalType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext

SCHEMA_FACTORY = '__schema_factory__'


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def create(self, type_: Type, json_context: JsonSchemaContext) -> Optional[SchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(json_context)
