from enum import Enum
from typing import Type, Optional, Dict

from schema.enum_schema import EnumSchema
from schema.factory.schema_factory_abc import SchemaFactoryABC, T

from schema.schema_abc import SchemaABC
from schema.schema_context import SchemaContext

PERMITTED_TYPES = [str, bool, int, float, (None).__class__]


class EnumSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], context: SchemaContext, defs: Dict[str, SchemaABC]) -> Optional[SchemaABC[T]]:
        if issubclass(type_, Enum):
            values = tuple(t.value for t in type_)
            if next((v for v in values if v.__class__ not in PERMITTED_TYPES), None) is None:
                return EnumSchema(values)
