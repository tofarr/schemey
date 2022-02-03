from typing import Type, Optional, Set, Union

from marshy import ExternalType
from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory

from schemey.any_of_schema import AnyOfSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.json_schema_abc import NoDefault, JsonSchemaABC
from schemey.schemey_context import SchemeyContext


class ImplSchemaFactory(SchemaFactoryABC):

    def create(self,
               type_: Type,
               context: SchemeyContext,
               default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
               ) -> Optional[JsonSchemaABC]:
        impls = self.get_impls(type_, context)
        if impls:
            schemas = tuple(context.get_schema(i).json_schema for i in impls)
            return AnyOfSchema(
                schemas=schemas,
                default_value=default_value,
                name=type_.__name__
            )

    def get_impls(self, type_: Type, context: SchemeyContext) -> Optional[Set[Type]]:
        factories = context.marshaller_context.get_factories()
        for factory in factories:
            if isinstance(factory, ImplMarshallerFactory):
                if factory.base == type_:
                    return factory.impls
