from datetime import datetime
from typing import Optional, Dict, Type

from schema.boolean_schema import BooleanSchema
from schema.factory.enum_schema_factory import EnumSchemaFactory

from schema.factory.schema_factory_abc import SchemaFactoryABC
from schema.null_schema import NullSchema
from schema.schema_abc import SchemaABC
from schema.schema_context import SchemaContext
from schema.string_schema import StringSchema
from schema.string_format import StringFormat
from schema.number_schema import NumberSchema
from schema.factory.any_of_schema_factory import AnyOfSchemaFactory
from schema.factory.array_schema_factory import ArraySchemaFactory
from schema.factory.factory_schema_factory import FactorySchemaFactory
from schema.factory.dataclass_schema_factory import DataclassSchemaFactory


class DefaultSchemaContext(SchemaContext):

    def __init__(self,
                 factories: Optional[SchemaFactoryABC] = None,
                 by_type: Optional[Dict[Type, SchemaABC]] = None):
        super().__init__(factories, by_type)
        self.register_schema(bool, BooleanSchema())
        self.register_schema(datetime, StringSchema(format=StringFormat.DATE_TIME))
        self.register_schema(float, NumberSchema[float](float))
        self.register_schema(int, NumberSchema[int](int))
        self.register_schema(str, StringSchema())
        self.register_schema((None).__class__, NullSchema())

        self.register_factory(AnyOfSchemaFactory())
        self.register_factory(ArraySchemaFactory())
        self.register_factory(FactorySchemaFactory())
        self.register_factory(DataclassSchemaFactory())
        self.register_factory(EnumSchemaFactory())
