from typing import Optional, Type, Union

from marshy import ExternalType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.schemey_context import SchemeyContext

SCHEMA_FACTORY = '__schema_factory__'


class FactorySchemaFactory(SchemaFactoryABC):
    priority: int = 110

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(default_value, context)
