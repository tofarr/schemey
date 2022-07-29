from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.datetime_factory import DatetimeFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.external_type_factory import ExternalTypeFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.factory.impl_schema_factory import ImplSchemaFactory
from schemey.factory.ref_schema_factory import RefSchemaFactory
from schemey.factory.simple_type_factory import SimpleTypeFactory
from schemey.factory.tuple_schema_factory import TupleSchemaFactory
from schemey.factory.uuid_factory import UuidFactory
from schemey.schema_context import SchemaContext

priority = 100


def configure(context: SchemaContext):
    context.register_factory(RefSchemaFactory())
    context.register_factory(SimpleTypeFactory(bool, "boolean"))
    context.register_factory(SimpleTypeFactory(int, "integer"))
    context.register_factory(SimpleTypeFactory(type(None), "null"))
    context.register_factory(SimpleTypeFactory(float, "number"))
    context.register_factory(SimpleTypeFactory(str, "string"))
    context.register_factory(DatetimeFactory())
    context.register_factory(UuidFactory())
    context.register_factory(ArraySchemaFactory())
    context.register_factory(TupleSchemaFactory())
    context.register_factory(ExternalTypeFactory())
    context.register_factory(DataclassSchemaFactory())
    context.register_factory(EnumSchemaFactory())
    context.register_factory(FactorySchemaFactory())
    context.register_factory(ImplSchemaFactory())
    context.register_factory(AnyOfSchemaFactory())
