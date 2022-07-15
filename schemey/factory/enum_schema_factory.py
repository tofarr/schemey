from enum import Enum
from inspect import isclass
from typing import Type, Optional

from schemey.enum_schema import EnumSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC
from schemey.schema_abc import SchemaABC
from schemey.json_schema_context import JsonSchemaContext


class EnumSchemaFactory(SchemaFactoryABC):
    def create(
        self, type_: Type, json_context: JsonSchemaContext
    ) -> Optional[SchemaABC]:
        if isclass(type_) and issubclass(type_, Enum):
            # noinspection PyTypeChecker
            return EnumSchema(enum={e.value for e in type_}, name=type_.__name__)
