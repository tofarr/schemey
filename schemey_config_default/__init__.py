from schemey.boolean_schema import BooleanSchema
from schemey.datetime_schema import DatetimeSchema
from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schema_context import SchemaContext
from schemey.schema_key import SchemaKey
from schemey.string_schema import StringSchema

priority = 100


def configure(context: SchemaContext):
    context.register_schema(BooleanSchema(), SchemaKey(bool, None))
    context.register_schema(BooleanSchema())
    context.register_schema(BooleanSchema(True))
    context.register_schema(DatetimeSchema())
    context.register_schema(NumberSchema[float](float))
    context.register_schema(NumberSchema[int](int))
    context.register_schema(StringSchema())
    # noinspection PyUnresolvedReferences
    context.register_schema(NullSchema())

    context.register_factory(AnyOfSchemaFactory())
    context.register_factory(ArraySchemaFactory())
    context.register_factory(FactorySchemaFactory())
    context.register_factory(DataclassSchemaFactory())
    context.register_factory(EnumSchemaFactory())
