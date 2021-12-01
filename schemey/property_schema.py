from dataclasses import dataclass
from typing import TypeVar, Generic, Iterator, Optional, List, TextIO

from marshy.types import ExternalItemType

from schemey.any_of_schema import strip_optional
from schemey.array_schema import ArraySchema
from schemey.graphql import PRIMITIVE_TYPES
from schemey.json_output_context import JsonOutputContext
from schemey.schema_abc import SchemaABC, T
from schemey.schema_error import SchemaError

B = TypeVar('B')
OBJECT = 'object'


@dataclass(frozen=True)
class PropertySchema(Generic[T, B], SchemaABC[T]):
    name: str
    schema: SchemaABC
    required: bool = False

    def get_schema_errors(self, item: T, current_path: Optional[List[str]] = None) -> Iterator[SchemaError]:
        if current_path is None:
            current_path = []
        if hasattr(item, 'get'):
            attr = item.get(self.name)
        else:
            attr = getattr(item, self.name, None)
        current_path.append(self.name)
        yield from self.schema.get_schema_errors(attr, current_path)
        current_path.pop()

    def to_json_schema(self, json_output_context: Optional[JsonOutputContext] = None) -> Optional[ExternalItemType]:
        return self.schema.to_json_schema(json_output_context)

    @property
    def item_type(self):
        return self.schema.item_type

    @property
    def default_value(self):
        return self.schema.default_value

    def to_graphql(self, writer: TextIO):
        writer.write(f'\t{self.name}: {get_graphql_type_name(self.schema)}\n')


def get_graphql_type_name(schema: SchemaABC):
    s = strip_optional(schema)
    required = schema is s
    is_array = isinstance(s, ArraySchema)
    if is_array:
        # noinspection PyUnresolvedReferences
        type_name = f'[{get_graphql_type_name(s.item_schema)}]'
    else:
        type_name = PRIMITIVE_TYPES.get(s.item_type) or s.item_type.__name__
    if required:
        type_name += '!'
    return type_name
