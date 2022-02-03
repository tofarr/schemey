from datetime import datetime, date
from uuid import UUID

from schemey.boolean_schema import BooleanSchema
from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.factory.impl_schema_factory import ImplSchemaFactory
from schemey.factory.type_schema_factory import TypeSchemaFactory
from schemey.integer_schema import IntegerSchema
from schemey.jsonifier.any_of_schema_jsonifier import AnyOfSchemaJsonifier
from schemey.jsonifier.array_schema_jsonifier import ArraySchemaJsonifier
from schemey.jsonifier.boolean_schema_jsonifier import BooleanSchemaJsonifier
from schemey.jsonifier.enum_schema_jsonifier import EnumSchemaJsonifier
from schemey.jsonifier.integer_schema_jsonifier import IntegerSchemaJsonifier
from schemey.jsonifier.null_schema_jsonifier import NullSchemaJsonifier
from schemey.jsonifier.number_schema_jsonifier import NumberSchemaJsonifier
from schemey.jsonifier.object_schema_jsonifier import ObjectSchemaJsonifier
from schemey.jsonifier.ref_schema_jsonifier import RefSchemaJsonifier
from schemey.jsonifier.string_schema_jsonifier import StringSchemaJsonifier
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schemey_context import SchemeyContext
from schemey.string_schema import StringSchema, date_string_schema, uuid_string_schema

priority = 100


def configure(context: SchemeyContext):
    configure_factories(context)
    configure_jsonifiers(context)


def configure_factories(context: SchemeyContext):
    context.register_factory(EnumSchemaFactory())
    context.register_factory(TypeSchemaFactory(bool, BooleanSchema))
    context.register_factory(TypeSchemaFactory(int, IntegerSchema))
    context.register_factory(TypeSchemaFactory(type(None), NullSchema))
    context.register_factory(TypeSchemaFactory(float, NumberSchema))
    context.register_factory(TypeSchemaFactory(str, StringSchema))
    context.register_factory(TypeSchemaFactory(datetime, date_string_schema))
    context.register_factory(TypeSchemaFactory(UUID, uuid_string_schema))
    context.register_factory(ArraySchemaFactory())
    context.register_factory(DataclassSchemaFactory())
    context.register_factory(EnumSchemaFactory())
    context.register_factory(FactorySchemaFactory())
    context.register_factory(ImplSchemaFactory())
    context.register_factory(AnyOfSchemaFactory())


def configure_jsonifiers(context: SchemeyContext):
    context.register_jsonifier(AnyOfSchemaJsonifier())
    context.register_jsonifier(ArraySchemaJsonifier())
    context.register_jsonifier(BooleanSchemaJsonifier())
    context.register_jsonifier(EnumSchemaJsonifier())
    context.register_jsonifier(IntegerSchemaJsonifier())
    context.register_jsonifier(NullSchemaJsonifier())
    context.register_jsonifier(NumberSchemaJsonifier())
    context.register_jsonifier(ObjectSchemaJsonifier())
    context.register_jsonifier(RefSchemaJsonifier())
    context.register_jsonifier(StringSchemaJsonifier())
