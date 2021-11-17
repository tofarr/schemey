from enum import Enum
from typing import Type, Optional

from schemey.enum_schema import EnumSchema
from schemey.factory.schema_factory_abc import SchemaFactoryABC, T, NONE_TYPE

from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext

PERMITTED_TYPES = [str, bool, int, float, NONE_TYPE]


class EnumSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], default_value: T, context: SchemaContext) -> Optional[SchemaABC[T]]:
        if issubclass(type_, Enum):
            return EnumSchema(type_, default_value=default_value)
