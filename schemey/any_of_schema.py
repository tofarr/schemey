from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Union, Sized, Type

from marshy.types import ExternalType

from schemey.json_schema_abc import JsonSchemaABC, NoDefault
from schemey.null_schema import NullSchema
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(JsonSchemaABC):
    schemas: Union[Iterable[JsonSchemaABC], Sized]
    default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
    name: str = None

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

    def get_schema_errors(self, item: ExternalType, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        errors = [SchemaError(current_path or [], 'type', item)]
        for schema in self.schemas:
            errors = list(schema.get_schema_errors(item, current_path))
            if not errors:
                return
        if item is not None:
            yield from errors


def optional_schema(schema: JsonSchemaABC,
                    default_value: Union[ExternalType, Type[NoDefault]] = NoDefault
                    ) -> JsonSchemaABC:
    return AnyOfSchema((NullSchema(), schema), default_value)


def strip_optional(schema: JsonSchemaABC) -> JsonSchemaABC:
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
