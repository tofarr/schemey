from dataclasses import dataclass
from typing import Type, Optional, Set, Dict

from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory
from marshy.types import ExternalItemType

from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema import Schema
from schemey.schema_context import SchemaContext


@dataclass
class ImplSchemaFactory(SchemaFactoryABC):
    """
    Schema factory which generates schemas for base classes with implementations
    as set up in marshy. There is no facility for turning this back into a class
    structure - though the UnionFactory will make a reasonably standardized class
    structure from the result.
    """

    priority: int = 150

    def from_type(
        self,
        type_: Type,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        impls = self.get_impls(type_, context)
        if impls:
            impls = sorted(list(impls), key=lambda i: i.__name__)
            any_of = []
            for impl in impls:
                prefix_items = [
                    {"const": impl.__name__},
                    context.schema_from_type(
                        impl, f"{path}/anyOf/{len(any_of)}/prefixItems/1", ref_schemas
                    ).schema,
                ]
                any_of.append(
                    {"type": "array", "prefixItems": prefix_items, "items": False}
                )
            # We overload the name annotation here to try and identify the impl when reading...
            return Schema({"name": type_.__name__, "anyOf": any_of}, type_)

    def from_json(
        self,
        item: ExternalItemType,
        context: SchemaContext,
        path: str,
        ref_schemas: Dict[Type, Schema],
    ) -> Optional[Schema]:
        """We read any named anyOf schema, and simply use what is defined locally rather than in the schema"""
        name = item.get("name")
        if not name or not item.get("anyOf"):
            return
        factories = context.marshaller_context.get_factories()
        for factory in factories:
            if isinstance(factory, ImplMarshallerFactory):
                if factory.base.__name__ == name:
                    schema = self.from_type(factory.base, context, path, ref_schemas)
                    return schema

    @staticmethod
    def get_impls(type_: Type, context: SchemaContext) -> Optional[Set[Type]]:
        factories = context.marshaller_context.get_factories()
        for factory in factories:
            if isinstance(factory, ImplMarshallerFactory):
                if factory.base == type_:
                    return factory.impls
