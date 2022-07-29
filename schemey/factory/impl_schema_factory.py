from dataclasses import dataclass
from typing import Type, Optional, Set, List, Dict

from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


@dataclass
class ImplSchemaFactory(SchemaFactoryABC):
    priority: int = 150

    def from_type(
        self, type_: Type, context: SchemaContext, path: str
    ) -> Optional[Schema]:
        impls = self.get_impls(type_, context)
        if impls:
            schemas = {
                "anyOf": [
                    context.schema_from_type(t, f"{path}/anyOf/{i}")
                    for i, t in enumerate(impls)
                ]
            }
            return Schema(schemas, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[str, Schema],
    ) -> Optional[Schema]:
        """No implementation"""

    @staticmethod
    def get_impls(type_: Type, context: SchemaContext) -> Optional[Set[Type]]:
        factories = context.marshaller_context.get_factories()
        for factory in factories:
            if isinstance(factory, ImplMarshallerFactory):
                if factory.base == type_:
                    return factory.impls
