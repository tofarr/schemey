from dataclasses import dataclass
from typing import Optional, List, Iterator, Iterable, Union, TextIO, Type

from marshy.types import ExternalItemType

from schemey.graphql import PRIMITIVE_TYPES
from schemey.graphql_context import GraphqlContext
from schemey.json_output_context import JsonOutputContext
from schemey.null_schema import NullSchema
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError


@dataclass(frozen=True)
class AnyOfSchema(SchemaABC[T]):
    schemas: Iterable[SchemaABC]
    default_value: Optional[T] = None
    name: str = None

    def __post_init__(self):
        schemas = []
        for s in self.schemas:
            if isinstance(s, AnyOfSchema):
                schemas.extend(s.schemas)
            else:
                schemas.append(s)
        object.__setattr__(self, 'schemas', tuple(schemas))
        if self.name is None:
            names = (_graphql_type_name(s.item_type) for s in self.schemas if not isinstance(s, NullSchema))
            object.__setattr__(self, 'name', f"AnyOf{''.join(name for name in names)}")

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

    def to_graphql_schema(self, target: GraphqlContext):
        schemas = [s for s in self.schemas if s != NullSchema()]
        if len(schemas) == 1:
            return schemas[0].to_graphql_schema(target)
        target.unions[self.name] = self
        for schema in self.schemas:
            schema.to_graphql_schema(target)

    def to_graphql(self, writer: TextIO):
        writer.write(f"union {self.name} = {' | '.join(_graphql_type_name(s.item_type) for s in self.schemas)}\n")


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


def _graphql_type_name(type_: Type):
    type_name = PRIMITIVE_TYPES.get(type_)
    if type_name:
        return type_name
    return type_.__name__
