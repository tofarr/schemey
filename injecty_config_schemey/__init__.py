from injecty import InjectyContext
from marshy.marshaller.marshaller_abc import MarshallerABC

from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.datetime_factory import DatetimeFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.external_type_factory import ExternalTypeFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.factory.impl_schema_factory import ImplSchemaFactory
from schemey.factory.ref_schema_factory import RefSchemaFactory
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.factory.simple_type_factory import (
    BoolTypeFactory,
    IntTypeFactory,
    NoneTypeFactory,
    FloatFactory,
    StrFactory,
)
from schemey.factory.tuple_schema_factory import TupleSchemaFactory
from schemey.factory.uuid_factory import UuidFactory
from schemey.json_schema.ranges_validator import RangesValidator
from schemey.json_schema.schema_validator_abc import SchemaValidatorABC
from schemey.json_schema.timestamp_validator import TimestampValidator
from schemey.schema_marshaller import SchemaMarshaller

priority = 100


def configure(context: InjectyContext):
    context.register_impl(MarshallerABC, SchemaMarshaller)
    context.register_impls(
        SchemaFactoryABC,
        [
            RefSchemaFactory,
            BoolTypeFactory,
            IntTypeFactory,
            NoneTypeFactory,
            FloatFactory,
            StrFactory,
            DatetimeFactory,
            UuidFactory,
            ArraySchemaFactory,
            TupleSchemaFactory,
            ExternalTypeFactory,
            DataclassSchemaFactory,
            EnumSchemaFactory,
            FactorySchemaFactory,
            ImplSchemaFactory,
            AnyOfSchemaFactory,
        ],
    )

    context.register_impls(
        SchemaValidatorABC,
        [
            RangesValidator,
            TimestampValidator,
        ],
    )
