from typing import Optional, Type, Union

from marshy import ExternalType

from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schemey_context import SchemeyContext

SCHEMA_FACTORY = '__schema_factory__'


class FactoryJsonSchemaFactory(JsonSchemaFactoryABC):
    priority: int = 110

    def create(self,
               type_: Type,
               json_context: JsonSchemaContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        factory = getattr(type_, SCHEMA_FACTORY, None)
        if factory is not None:
            return factory(default, json_context)
