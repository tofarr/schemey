from dataclasses import dataclass
from typing import TypeVar, Generic, Iterator, Optional, List

from marshy.types import ExternalItemType

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
