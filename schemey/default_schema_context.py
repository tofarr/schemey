from typing import Optional, Dict, Type

from schemey.boolean_schema import BooleanSchema
from schemey.datetime_schema import DatetimeSchema
from schemey.factory.any_of_schema_factory import AnyOfSchemaFactory
from schemey.factory.array_schema_factory import ArraySchemaFactory
from schemey.factory.dataclass_schema_factory import DataclassSchemaFactory
from schemey.factory.enum_schema_factory import EnumSchemaFactory
from schemey.factory.factory_schema_factory import FactorySchemaFactory
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.null_schema import NullSchema
from schemey.number_schema import NumberSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext
from schemey.schema_key import SchemaKey
from schemey.string_schema import StringSchema


class DefaultSchemaContext(SchemaContext):

    def __init__(self,
                 factories: Optional[SchemaFactoryABC] = None,
                 by_type: Optional[Dict[Type, SchemaABC]] = None):
        super().__init__(factories, by_type)

        self.register_schema(BooleanSchema(), SchemaKey(bool, None))
        self.register_schema(BooleanSchema())
        self.register_schema(BooleanSchema(True))
        self.register_schema(DatetimeSchema())
        self.register_schema(NumberSchema[float](float))
        self.register_schema(NumberSchema[int](int))
        self.register_schema(StringSchema())
        # noinspection PyUnresolvedReferences
        self.register_schema(NullSchema())

        self.register_factory(AnyOfSchemaFactory())
        self.register_factory(ArraySchemaFactory())
        self.register_factory(FactorySchemaFactory())
        self.register_factory(DataclassSchemaFactory())
        self.register_factory(EnumSchemaFactory())
