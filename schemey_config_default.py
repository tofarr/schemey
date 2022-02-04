from datetime import datetime
from uuid import UUID

from schemey.boolean_schema import BooleanSchema
from schemey.factory.any_of_schema_factory import AnyOfJsonSchemaFactory
from schemey.factory.array_schema_factory import ArrayJsonSchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassJsonSchemaFactory
from schemey.factory.enum_schema_factory import EnumJsonSchemaFactory
from schemey.factory.factory_schema_factory import FactoryJsonSchemaFactory
from schemey.factory.impl_schema_factory import ImplJsonSchemaFactory
from schemey.factory.type_schema_factory import TypeJsonSchemaFactory
from schemey.integer_schema import IntegerSchema
from schemey.loader.any_of_schema_loader import AnyOfSchemaLoader
from schemey.loader.array_schema_loader import ArraySchemaLoader
from schemey.loader.boolean_schema_loader import BooleanSchemaLoader
from schemey.loader.enum_schema_loader import EnumSchemaLoader
from schemey.loader.integer_schema_loader import IntegerSchemaLoader
from schemey.loader.null_schema_loader import NullSchemaLoader
from schemey.loader.number_schema_loader import NumberSchemaLoader
from schemey.loader.object_schema_loader import ObjectSchemaLoader
from schemey.loader.ref_schema_loader import RefSchemaLoader
from schemey.loader.string_schema_loader import StringSchemaLoader
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schemey_context import SchemeyContext
from schemey.string_schema import StringSchema, date_string_schema, uuid_string_schema

priority = 100


def configure(context: SchemeyContext):
    configure_factories(context)
    configure_loaders(context)


def configure_factories(context: SchemeyContext):
    context.register_factory(EnumJsonSchemaFactory())
    context.register_factory(TypeJsonSchemaFactory(bool, BooleanSchema))
    context.register_factory(TypeJsonSchemaFactory(int, IntegerSchema))
    context.register_factory(TypeJsonSchemaFactory(type(None), NullSchema))
    context.register_factory(TypeJsonSchemaFactory(float, NumberSchema))
    context.register_factory(TypeJsonSchemaFactory(str, StringSchema))
    context.register_factory(TypeJsonSchemaFactory(datetime, date_string_schema))
    context.register_factory(TypeJsonSchemaFactory(UUID, uuid_string_schema))
    context.register_factory(ArrayJsonSchemaFactory())
    context.register_factory(DataclassJsonSchemaFactory())
    context.register_factory(EnumJsonSchemaFactory())
    context.register_factory(FactoryJsonSchemaFactory())
    context.register_factory(ImplJsonSchemaFactory())
    context.register_factory(AnyOfJsonSchemaFactory())


def configure_loaders(context: SchemeyContext):
    context.register_loader(AnyOfSchemaLoader())
    context.register_loader(ArraySchemaLoader())
    context.register_loader(BooleanSchemaLoader())
    context.register_loader(EnumSchemaLoader())
    context.register_loader(IntegerSchemaLoader())
    context.register_loader(NullSchemaLoader())
    context.register_loader(NumberSchemaLoader())
    context.register_loader(ObjectSchemaLoader())
    context.register_loader(RefSchemaLoader())
    context.register_loader(StringSchemaLoader())
