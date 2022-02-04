from typing import Type, Optional, Set, Union

from marshy import ExternalType
from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory

from schemey.any_of_schema import AnyOfSchema
from schemey.factory.json_schema_factory_abc import JsonSchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.schemey_context import SchemeyContext


class ImplJsonSchemaFactory(JsonSchemaFactoryABC):

    def create(self,
               type_: Type,
               json_context: JsonSchemaContext,
               default: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        impls = self.get_impls(type_, json_context)
        if impls:
            schemas = tuple(json_context.create_schema(i) for i in impls)
            return AnyOfSchema(
                schemas=schemas,
                default=default,
                name=type_.__name__
            )

    def get_impls(self, type_: Type, json_context: JsonSchemaContext) -> Optional[Set[Type]]:
        factories = json_context.marshaller_context.get_factories()
        for factory in factories:
            if isinstance(factory, ImplMarshallerFactory):
                if factory.base == type_:
                    return factory.impls
