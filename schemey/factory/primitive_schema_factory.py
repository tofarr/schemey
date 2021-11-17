from dataclasses import dataclass
from typing import Type, Optional, Dict, TypeVar

from schemey.factory.schema_factory_abc import SchemaFactoryABC, T
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext

S = TypeVar('S', bound=SchemaABC)


@dataclass(frozen=True)
class PrimitiveSchemaFactory(SchemaFactoryABC):
    schema_types_by_type: Dict[Type, Type[S]]

    def create(self, type_: Type[T], default_value: Optional[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        schema_type = self.schema_types_by_type.get(type_)
        if schema_type:
            schema = schema_type(default_value=default_value)
            return schema
