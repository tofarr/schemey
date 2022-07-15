from dataclasses import dataclass
from typing import Type, Optional, Set

from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory

from schemey.any_of_schema import AnyOfSchema
from schemey.const_schema import ConstSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext
from schemey.tuple_schema import TupleSchema


@dataclass
class ImplSchemaFactory(SchemaFactoryABC):
    priority: int = 150

    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        impls = self.get_impls(type_, json_context)
        if impls:
            schemas = tuple(self.wrap_impl(i, json_context) for i in impls)
            return AnyOfSchema(schemas=schemas, name=type_.__name__)

    @staticmethod
    def get_impls(type_: Type, json_context: JsonSchemaContext) -> Optional[Set[Type]]:
        factories = json_context.marshaller_context.get_factories()
        for factory in factories:
            if isinstance(factory, ImplMarshallerFactory):
                if factory.base == type_:
                    return factory.impls

    @staticmethod
    def wrap_impl(type_: Type, json_context: JsonSchemaContext):
        schema = json_context.get_schema(type_)
        schema = TupleSchema((ConstSchema(type_.__name__), schema))
        return schema
