from datetime import datetime
from uuid import UUID

from schemey.boolean_schema import BooleanSchema
from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.factory.impl_schema_factory import ImplSchemaFactory
from schemey.factory.tuple_schema_factory import TupleSchemaFactory
from schemey.integer_schema import IntegerSchema
from schemey.loader.any_of_schema_loader import AnyOfSchemaLoader
from schemey.loader.array_schema_loader import ArraySchemaLoader
from schemey.loader.boolean_schema_loader import BooleanSchemaLoader
from schemey.loader.const_schema_loader import ConstSchemaLoader
from schemey.loader.enum_schema_loader import EnumSchemaLoader
from schemey.loader.integer_schema_loader import IntegerSchemaLoader
from schemey.loader.null_schema_loader import NullSchemaLoader
from schemey.loader.number_schema_loader import NumberSchemaLoader
from schemey.loader.object_schema_loader import ObjectSchemaLoader
from schemey.loader.ref_schema_loader import RefSchemaLoader
from schemey.loader.string_schema_loader import StringSchemaLoader
from schemey.loader.tuple_schema_loader import TupleSchemaLoader
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schema_context import SchemaContext
from schemey.string_format import StringFormat
from schemey.string_schema import StringSchema

priority = 100


def configure(context: SchemaContext):
    configure_schemas(context)
    configure_factories(context)
    configure_loaders(context)


def configure_schemas(context: SchemaContext):
    context.register_schema(bool, BooleanSchema())
    context.register_schema(int, IntegerSchema())
    context.register_schema(type(None), NullSchema())
    context.register_schema(float, NumberSchema())
    context.register_schema(str, StringSchema())
    context.register_schema(datetime, StringSchema(format=StringFormat.DATE_TIME))
    context.register_schema(UUID, StringSchema(format=StringFormat.UUID))


def configure_factories(context: SchemaContext):
    context.register_factory(EnumSchemaFactory())
    context.register_factory(ArraySchemaFactory())
    context.register_factory(TupleSchemaFactory())
    context.register_factory(DataclassSchemaFactory())
    context.register_factory(EnumSchemaFactory())
    context.register_factory(FactorySchemaFactory())
    context.register_factory(ImplSchemaFactory())
    context.register_factory(AnyOfSchemaFactory())


def configure_loaders(context: SchemaContext):
    context.register_loader(AnyOfSchemaLoader())
    context.register_loader(ArraySchemaLoader())
    context.register_loader(BooleanSchemaLoader())
    context.register_loader(ConstSchemaLoader())
    context.register_loader(EnumSchemaLoader())
    context.register_loader(IntegerSchemaLoader())
    context.register_loader(NullSchemaLoader())
    context.register_loader(NumberSchemaLoader())
    context.register_loader(ObjectSchemaLoader())
    context.register_loader(RefSchemaLoader())
    context.register_loader(StringSchemaLoader())
    context.register_loader(TupleSchemaLoader())
