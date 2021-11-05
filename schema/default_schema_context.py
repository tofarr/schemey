from datetime import datetime
from typing import Optional, Dict, Type

from persisty.schema.boolean_schema import BooleanSchema

from persisty.schema.factory.schema_factory_abc import SchemaFactoryABC
from persisty.schema.schema_abc import SchemaABC
from persisty.schema.schema_context import SchemaContext
from persisty.schema.string_schema import StringSchema
from persisty.schema.string_format import StringFormat
from persisty.schema.number_schema import NumberSchema
from persisty.schema.factory.optional_schema_factory import OptionalSchemaFactory
from persisty.schema.factory.array_schema_factory import ArraySchemaFactory
from persisty.schema.factory.factory_schema_factory import FactorySchemaFactory
from persisty.schema.factory.dataclass_schema_factory import DataclassSchemaFactory


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

        self.register_factory(OptionalSchemaFactory())
        self.register_factory(ArraySchemaFactory())
        self.register_factory(FactorySchemaFactory())
        self.register_factory(DataclassSchemaFactory())
