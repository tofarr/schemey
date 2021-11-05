from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable

from marshy.types import ExternalType

from persisty.schema.null_schema import NullSchema
from persisty.schema.schema_abc import SchemaABC, T
from persisty.schema.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(SchemaABC[T]):
    schemas: Iterable[SchemaABC]

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        errors = [SchemaError(current_path or [], 'type', item)]
        for schema in self.schemas:
            errors = list(schema.get_schema_errors(item, current_path))
            if not errors:
                return
        if item is not None:
            yield from errors


def optional_schema(schema: SchemaABC) -> SchemaABC:
    return AnyOfSchema((NullSchema(), schema))


def strip_optional(schema: SchemaABC) -> SchemaABC:
    if not isinstance(schema, AnyOfSchema):
        return schema
    schemas = list(schema.schemas)
    if len(schemas) != 2:
        return schema
    if isinstance(schemas[0], NullSchema):
        return schemas[1]
    if isinstance(schemas[0], NullSchema):
        return schemas[0]
    return schema
