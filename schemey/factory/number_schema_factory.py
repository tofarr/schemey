from dataclasses import dataclass
from typing import Type, Optional

from schemey.factory.schema_factory_abc import SchemaFactoryABC, T
from schemey.number_schema import NumberSchema
from schemey.schema_abc import SchemaABC
from schemey.schema_context import SchemaContext


@dataclass(frozen=True)
class NumberSchemaFactory(SchemaFactoryABC):

    def create(self, type_: Type[T], default_value: Optional[T], context: SchemaContext) -> Optional[SchemaABC[T]]:
        if type_ in [int, float]:
            schema = NumberSchema(type_, default_value=default_value)
            return schema
