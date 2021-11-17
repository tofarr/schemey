from datetime import datetime
from uuid import UUID

from schemey.boolean_schema import BooleanSchema
from schemey.datetime_schema import DatetimeSchema
from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.factory.number_schema_factory import NumberSchemaFactory
from schemey.factory.primitive_schema_factory import PrimitiveSchemaFactory
from schemey.null_schema import NullSchema
from schemey.schema_context import SchemaContext
from schemey.string_schema import StringSchema
from schemey.uuid_schema import UuidSchema

priority = 100


def configure(context: SchemaContext):
    # noinspection PyUnresolvedReferences
    context.register_schema(NullSchema())

    context.register_factory(AnyOfSchemaFactory())
    context.register_factory(ArraySchemaFactory())
    context.register_factory(FactorySchemaFactory())
    context.register_factory(DataclassSchemaFactory())
    context.register_factory(EnumSchemaFactory())
    context.register_factory(NumberSchemaFactory())
    context.register_factory(PrimitiveSchemaFactory({
        bool: BooleanSchema,
        datetime: DatetimeSchema,
        str: StringSchema,
        UUID: UuidSchema
    }))
