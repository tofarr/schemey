from dataclasses import dataclass, field
from typing import Type, Optional, Set

from marshy.factory.impl_marshaller_factory import ImplMarshallerFactory
from marshy.marshaller_context import MarshallerContext

from schemey.any_of_schema import AnyOfSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC, T
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext, get_default_schema_context


@dataclass
class ImplSchemaFactory(SchemaFactoryABC):
    base: Type[T]
    priority: int = 110
    impls: Set[Type[T]] = field(default_factory=set)
    default_value: T = None

    def create(self, type_: Type[T], default_value, schema_context: SchemaContext) -> Optional[SchemaABC[T]]:
        if type_ is self.base:
            return AnyOfSchema(schemas=tuple(schema_context.get_schema(i) for i in self.impls),
                               default_value=self.default_value,
                               name=self.base.__name__)

    def add_impl(self, impl):
        self.impls.add(impl)


def register_impl(base, impl, schema_context: Optional[SchemaContext] = None):
    if schema_context is None:
        schema_context = get_default_schema_context()
    for factory in schema_context.get_factories():
        if isinstance(factory, ImplSchemaFactory) and factory.base == base:
            factory.add_impl(impl)
            return
    factory = ImplSchemaFactory(base)
    factory.add_impl(impl)
    schema_context.register_factory(factory)


def register_marshy_impls(schema_context: SchemaContext, marshaller_context: Optional[MarshallerContext] = None):
    if marshaller_context is None:
        from marshy import get_default_context
        marshaller_context = get_default_context()
    for factory in marshaller_context.get_factories():
        if isinstance(factory, ImplMarshallerFactory):
            for impl in factory.impls:
                register_impl(factory.base, impl, schema_context)
