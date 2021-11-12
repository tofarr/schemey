from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Union

from marshy.types import ExternalItemType

from schemey.json_output_context import JsonOutputContext
from schemey.null_schema import NullSchema
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(SchemaABC[T]):
    schemas: Iterable[SchemaABC]
    default_value: Optional[T] = None

    def __post_init__(self):
        schemas = []
        for s in self.schemas:
            if isinstance(s, AnyOfSchema):
                schemas.extend(s.schemas)
            else:
                schemas.append(s)
        object.__setattr__(self, 'schemas', tuple(schemas))

    @property
    def item_type(self):
        types = tuple(s.item_type for s in self.schemas)
        return Union[types]

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        errors = [SchemaError(current_path or [], 'type', item)]
        for schema in self.schemas:
            errors = list(schema.get_schema_errors(item, current_path))
            if not errors:
                return
        if item is not None:
            yield from errors

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        dumped = dict(anyOf=[s.to_json_schema(json_output_context) for s in self.schemas])
        return dumped


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
    if isinstance(schemas[1], NullSchema):
        return schemas[0]
    return schema
